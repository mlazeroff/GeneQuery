import os
import time
import requests
from ruamel import yaml

RAST_URL = 'http://pubseed.theseed.org/rast/server.cgi'


class Rast:
    """
    Class for representing queries to RAST annotation servers
    """
    class RastException(Exception):
        pass

    def __init__(self, username: str, password: str):
        """
        :param username:
        :param password:
        """
        self.username = username
        self.password = password
        self.file = None
        self.jobId = None
        self.status = None

    def submit(self, filePath: str, sequenceName: str):
        """
        Submits a file for annotation
        :param filePath: name of a fasta file
        :param sequenceName: name of the sequence
        Raises an exception if not successful
        """
        _SUBMIT_FUNCTION = 'submit_RAST_job'

        # check if file exists
        if not os.path.exists(filePath):
            raise FileNotFoundError('\"{}\" does not exist'.format(filePath))

        # attempt to submit file
        with open(filePath) as file:
            fastaContent = file.read()

        # submit args
        args = yaml.dump({'-determineFamily': 0,
                          '-domain': 'Bacteria',
                          '-filetype': 'fasta',
                          '-geneCaller': 'RAST',
                          '-geneticCode': 11,
                          '-keepGeneCalls': 0,
                          '-non_active': 0,
                          '-organismName': sequenceName,
                          '-taxonomyID': ''}, Dumper=yaml.RoundTripDumper)
        # create file content in yaml format
        file = '-file: |-\n'
        for line in fastaContent.splitlines():
            # two spaces indentation for inline string
            file += '  {}\n'.format(line)
        args += file

        payload = {'function': _SUBMIT_FUNCTION,
                   'args': args,
                   'username': self.username,
                   'password': self.password}

        submitReq = requests.post(RAST_URL, data=payload)
        submitReq.raise_for_status()

        submitResponse = yaml.safe_load(submitReq.text)
        if submitResponse['status'] == 'ok':
            self.jobId = submitResponse['job_id']
            self.status = 'incomplete'
        else:
            raise self.RastException('Received status response of :{}'.format(submitResponse['status']))

    def checkIfComplete(self):
        """
        Checks if the current job is complete
        :return: True/False
        """
        _SUCCESS_FIELD = 'status'
        _SUCCESSFUL_STATUS = 'complete'
        _CHECK_STATUS_FUNCTION = 'status_of_RAST_job'

        args = '---\n-job:\n  - {}\n'.format(self.jobId)
        payload = {'function': _CHECK_STATUS_FUNCTION,
                   'username': self.username,
                   'password': self.password,
                   'args': args}

        statusReq = requests.post(RAST_URL, data=payload)
        statusReq.raise_for_status()
        statusContent = yaml.safe_load(statusReq.text)
        jobStatus = statusContent[self.jobId][_SUCCESS_FIELD]
        self.status = jobStatus
        return True if jobStatus == _SUCCESSFUL_STATUS else False

    def retrieveData(self):
        """
        Retrieves the gff3 data for the associated job
        :return: gff3 content
        """
        _RETRIEVE_FUNCTION = 'retrieve_RAST_job'

        args = yaml.dump({'-format': 'gff3_stripped', '-job': self.jobId})
        payload = {'function': _RETRIEVE_FUNCTION,
                   'username': self.username,
                   'password': self.password,
                   'args': args}

        retrieveReq = requests.post(RAST_URL, data=payload)
        retrieveReq.raise_for_status()

        return retrieveReq.text


if __name__ == '__main__':
    rast = Rast('mlazeroff', 'chester')
    rast.submit("D:\mdlaz\Documents\College\Research\programs\GeneQuery\\tests\sequences\Ronan.fasta",
                'ROONAN')
    time.sleep(.5)
    print(rast.checkIfComplete())




