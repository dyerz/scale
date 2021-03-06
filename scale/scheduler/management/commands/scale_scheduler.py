import logging
import signal
import sys
from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand

from scheduler.scale_scheduler import ScaleScheduler

logger = logging.getLogger(__name__)

# Try to import production Mesos bindings, fall back to stubs
try:
    from mesos.interface import mesos_pb2
    from mesos.native import MesosSchedulerDriver
    logger.info(u'Successfully imported native Mesos bindings')
except ImportError:
    logger.info(u'No native Mesos bindings, falling back to stubs')
    import mesos_api.mesos_pb2 as mesos_pb2
    from mesos_api.mesos import MesosSchedulerDriver

#TODO: make these command options
MESOS_CHECKPOINT = False
MESOS_AUTHENTICATE = False
DEFAULT_PRINCIPLE = None
DEFAULT_SECRET = None


class Command(BaseCommand):
    '''Command that launches the Scale scheduler
    '''

    option_list = BaseCommand.option_list + (
        make_option('-m', '--master', action='store', type='str', default=settings.MESOS_MASTER,
                    help=('The master to connect to')),
    )

    help = 'Launches the Scale scheduler'

    def handle(self, **options):
        '''See :meth:`django.core.management.base.BaseCommand.handle`.

        This method starts the scheduler.
        '''

        # Register a listener to handle clean shutdowns
        signal.signal(signal.SIGTERM, self._onsigterm)

        # TODO: clean this up
        mesos_master = options.get('master')

        logger.info(u'Command starting: scale_scheduler')
        logger.info(u' - Master: %s', mesos_master)
        executor = mesos_pb2.ExecutorInfo()
        executor.executor_id.value = 'scale'
        executor.command.value = '%s %s scale_executor' % (settings.PYTHON_EXECUTABLE, settings.MANAGE_FILE)
        executor.name = 'Scale Executor (Python)'

        self.scheduler = ScaleScheduler(executor)

        framework = mesos_pb2.FrameworkInfo()
        framework.user = ''  # Have Mesos fill in the current user.
        framework.name = 'Scale Framework (Python)'

        # TODO(vinod): Make checkpointing the default when it is default on the slave.
        if MESOS_CHECKPOINT:
            logger.info('Enabling checkpoint for the framework')
            framework.checkpoint = True

        if MESOS_AUTHENTICATE:
            logger.info('Enabling authentication for the framework')

            if not DEFAULT_PRINCIPLE:
                logger.error('Expecting authentication principal in the environment')
                sys.exit(1)

            if not DEFAULT_SECRET:
                logger.error('Expecting authentication secret in the environment')
                sys.exit(1)

            credential = mesos_pb2.Credential()
            credential.principal = DEFAULT_PRINCIPLE
            credential.secret = DEFAULT_SECRET

            self.driver = MesosSchedulerDriver(self.scheduler, framework, mesos_master, credential)
        else:
            self.driver = MesosSchedulerDriver(self.scheduler, framework, mesos_master)

        status = 0 if self.driver.run() == mesos_pb2.DRIVER_STOPPED else 1

        # Perform any required clean up operations like stopping background threads
        status = status or self._shutdown()

        logger.info(u'Command completed: scale_scheduler')
        sys.exit(status)

    def _onsigterm(self, signum, _frame):
        '''See signal callback registration: :py:func:`signal.signal`.

        This callback performs a clean shutdown when a TERM signal is received.
        '''
        logger.info(u'Scheduler command terminated due to signal: %i', signum)
        self._shutdown()
        sys.exit(1)

    def _shutdown(self):
        '''Performs any clean up required by this command.

        :returns: The exit status code based on whether the shutdown operation was clean with no exceptions.
        :rtype: int
        '''
        status = 0

        try:
            if self.scheduler:
                self.scheduler.shutdown()
        except:
            logger.exception('Failed to properly shutdown scale scheduler.')
            status = 1

        try:
            if self.driver:
                self.driver.stop()
        except:
            logger.exception('Failed to properly stop Mesos driver.')
            status = 1
        return status
