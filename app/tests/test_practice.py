import pytest
from unittest import mock

class Worker:
    def work(self):
        return "work"


def test_practice():
    worker = Worker()
    with mock.patch.object(worker, 'work', return_value="mocking!!"):
        result = worker.work()
        print(result)

    with mock.patch.object(worker, 'work', side_effect=ValueError("mocking!!")):
        try:
            result = worker.work()
        except ValueError as err:
            message = str(err)
            print(message)
    result = worker.work()
    assert result == "work"
