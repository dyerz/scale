'''Defines the interface for translating a job's exit codes
to error types'''

import logging

from jsonschema import validate
from jsonschema.exceptions import ValidationError

from job.configuration.interface.exceptions import InvalidInterfaceDefinition

from error.models import Error

logger = logging.getLogger(__name__)

ERROR_INTERFACE_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "version": {
            "description": "version of the error_interface schema",
            "type": "string",
            "pattern": "^.{0,50}$"
        },
        "exit_codes": {
            "type": "object",
            "item": {
                "type": "string",
            }
        },
    },
}


class ErrorInterface(object):
    '''Represents the interface for translating a job's exit code to an error type'''

    def __init__(self, definition):
        '''Creates an error interface from the given definition.

        If the definition is invalid, a :class:`job.configuration.interface.exceptions.InvalidInterfaceDefinition`
        exception will be thrown.

        :param definition: The interface definition
        :type definition: dict
        '''
        if definition is None:
            definition = {}

        self.definition = definition

        try:
            validate(definition, ERROR_INTERFACE_SCHEMA)
        except ValidationError as validation_error:
            raise InvalidInterfaceDefinition(validation_error)

    def get_error(self, exit_code=None):
        ''' This method retrieves an error given an exit_code.

        :param exit_code: The exit code from a previously ran job.
        :type exit_code: int
        :returns: The error model mapped to the given exit code.
        :rtype: :class:`error.models.Error`
        '''

        error = None
        if exit_code is not None:
            # if the exit code is zero, None should be returned
            if exit_code == 0:
                return None

            # get the exit codes
            exit_codes = self.definition.get(u'exit_codes')
            if exit_codes:
                # Retrieve the error item using the exit code from the dict
                # exit code should never be None, but it may not be in 'exit_codes'
                error_name = exit_codes.get(str(exit_code))
                if error_name is not None:
                    # get the name to search for in the 'Error' database table
                    error = self._lookup_error(error_name)

        # Set the error to the 'Unknown' error as a fall back default
        if not error:
            if exit_code is None or exit_code != 0:
                error = Error.objects.get_unknown_error()
        return error

    def get_error_names(self):
        '''Returns a set of all error names for this interface

        :returns: Set of error names
        :rtype: set[string]
        '''
        if u'exit_codes' not in self.definition:
            return set()

        codes = self.definition.get(u'exit_codes')
        return {error_name for error_name in codes.itervalues()}

    def _lookup_error(self, name):
        '''This method looks up error by name

        :param name: The name of the error to retrieve
        :type name: string
        :return: The error model with the given name.
        :rtype: :class:`error.models.Error`
        '''
        try:
            return Error.objects.get(name=name)
        except Error.DoesNotExist:
            logger.exception('Unable to find error mapping: %s', name)
            pass
