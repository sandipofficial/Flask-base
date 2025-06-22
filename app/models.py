from flask import Flask, render_template, flash, request, url_for, redirect, session
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart
import MySQLdb.cursors
from flask_mysqldb import MySQL
import gc
from functools import wraps
from config import *
from app.__init__ import app
from app.__init__ import mysql

def access_task(taskid):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM user_has_task WHERE fk_task_id = %s", (taskid,))
    tmp = cursor.fetchone()
    return tmp

def get_info_for_task(taskid):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM task WHERE task_id = %s', (taskid,))
    data = cursor.fetchone()
    return data

def delete_task(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("DELETE FROM task WHERE task_id = %s", (id,))
    cursor.execute("DELETE FROM user_has_task WHERE fk_task_id = %s", (id,))
    mysql.connection.commit()

def add_task(title, content, end):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('INSERT INTO task(title, content, end) VALUES (%s, %s, %s)', (title, content, end,))
    mysql.connection.commit()
    cursor.execute("SELECT * FROM task WHERE task_id=(select max(task_id) from task)")
    res = cursor.fetchone()
    cursor.execute("INSERT INTO user_has_task VALUES (%s, %s)", (session['id'], res['task_id']))
    mysql.connection.commit()
    msg = 'You have successfully upload your task!'
    return msg

def get_all_tasks():
    table_id = []
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    res = cursor.execute('SELECT * FROM user_has_task WHERE fk_user_id = %s', (session['id'],))
    if res > 0:
        id = cursor.fetchone()
        while (id != None):
            table_id.append(id['fk_task_id'])
            id = cursor.fetchone()
    return table_id

def get_all_info_tasks(table_id):
    tasks = []
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    for values in table_id:
        cursor.execute("SELECT * FROM task WHERE task_id= %s", (values,))
        tmp = cursor.fetchone()
        tasks.append(tmp)
    return tasks

def login_function(username, password):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    res = cursor.execute('SELECT * FROM user WHERE username = %s AND password = %s', (username, password))
    account = cursor.fetchone()
    return res, account

def verify_if_user_exists(username):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM user WHERE username = %s', (username,))
    account = cursor.fetchone()
    return account

def register_function(username, password):
    msg = ""
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('INSERT INTO user(username, password) VALUES (%s, %s)', (username, password,))
    mysql.connection.commit()
    msg = 'You have successfully registered!'
    return msg

def edit_task(userid, task_id, title, content, end):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("UPDATE task SET title=%s, content=%s, end=%s WHERE userid=%s AND task_id=%s", (title, content, end, userid, task_id,))
    mysql.connection.commit()