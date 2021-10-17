import json
import log4p
import logging
from typing import List
from flask import request
from flask_restful import Resource

MOCKUP_DATA_FILE = "./mockup-data.json"

class TaskResources:
    def __init__(self):
        self._log = log4p.GetLogger(
            __file__.split("/")[-1], logging.DEBUG,
            config="./config/log4p.json"
        ).logger

    def _load_from_json_file(self) -> dict:
        with open(MOCKUP_DATA_FILE, "r") as file:
            data: dict = json.load(file)
        return data

    def _dump_to_json_file(self, data) -> dict:
        with open(MOCKUP_DATA_FILE, "w") as file:
            data = json.dump(data, file, indent=4)
        return data

    def _return_error(self, error, code): 
        self._log.error(f"APIError: {error}, code: {code}")
        return f"APIError: {error}", code


class GetTaskByAll(Resource, TaskResources):
    """
    Get all of the tasks.
    """
    def get(self):
        try:
            data = self._load_from_json_file();
            task_list = data["tasks"]
            return task_list, 200
        except Exception as exc:
            self._return_error(exc, 500)


class DeleteTaskById(Resource, TaskResources):
    """
    Delete a task by providing its ID.
    """
    def delete(self, taskId):
        try:
            data = self._load_from_json_file();
            tasks: List = data["tasks"]

            found = False
            for task in tasks:
                if task["id"] == taskId:
                    self._log.warn(f"Deleting task: {task}")
                    tasks.remove(task)
                    found = True
                    break
            if not found:
                self._return_error(f"Task with id {taskId} does not exist.", 404)

            data = self._dump_to_json_file(data)
            return f"Task with id {taskId} has been deleted.", 200
        except Exception as exc:
            self._return_error(exc, 500)


class UpdateTask(Resource, TaskResources):
    """
    Update properties of a task, keeping its ID
    """
    def put(self):
        try:
            req_body_string = request.data.decode()
            new_task: dict = json.loads(req_body_string)

            index = 0
            found = False
            data = self._load_from_json_file();
            tasks: List = data["tasks"]
            for task in tasks:
                if task["id"] == new_task["id"]:
                    # Remove and reinsert
                    self._log.info(f"Updating task: {task} to task {new_task}")
                    tasks.remove(task)
                    tasks.insert(index, new_task)
                    found = True
                    break
                index += 1
            if not found:
                self._return_error(f"Task with id {new_task['id']} does not exist.", 404)

            data = self._dump_to_json_file(data)
            tasks_list = GetTaskByAll().get()[0]
            return tasks_list[index], 200
        except Exception as exc:
            self._return_error(exc, 500)


class AddTask(Resource, TaskResources):
    """
    Insert a new task and return the entire object
    """
    def post(self):
        try:
            req_body_str = request.data.decode()
            new_task: dict = json.loads(req_body_str)

            ids = []
            data = self._load_from_json_file();
            tasks: List = data["tasks"]
            for task in tasks:
                ids.append(task["id"])
            next_id = max(ids) + 1

            new_task["id"] = next_id
            self._log.info(f"Adding task: {new_task}")
            tasks.append(new_task)
            data["tasks"] = tasks

            data = self._dump_to_json_file(data)
            return new_task, 200
        except Exception as exc:
            self._return_error(exc, 500)
