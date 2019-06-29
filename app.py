import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'bglynch-task_manager'
app.config['MONGO_URI'] = 'mongodb://admin:pa55word@ds147390.mlab.com:47390/bglynch-task_manager'

mongo = PyMongo(app)

@app.route('/')
@app.route('/get_tasks')
def get_tasks():
    return render_template("tasks.html", 
    tasks = mongo.db.tasks.find())


@app.route('/add_task')
def add_task():
    return render_template('addtask.html', 
    categories=mongo.db.categories.find() )


@app.route('/insert_task', methods=['POST'])
def insert_task():
    tasks = mongo.db.tasks
    task = request.form.to_dict()
    if 'is_urgent' not in task:
        task['is_urgent'] = False
    else:
        task['is_urgent'] = True
    tasks.insert_one(task)
    return redirect(url_for('get_tasks'))


@app.route('/edit_task/<task_id>')
def edit_task(task_id):
    the_task = mongo.db.tasks.find_one({'_id': ObjectId(task_id)})
    all_categories = mongo.db.categories.find()
    return render_template('edittask.html', 
        task=the_task, 
        categories=all_categories)


@app.route('/update_task/<task_id>', methods = ['POST'])
def update_task(task_id):
    tasks = mongo.db.tasks
    task = request.form.to_dict()
    if 'is_urgent' not in task:
        task['is_urgent'] = False
    else:
        task['is_urgent'] = True
    tasks.update({'_id': ObjectId(task_id)},
    {
        'task_name':task['task_name'],
        'category_name':task['category_name'],
        'task_discription':task['task_discription'],
        'due_date':task['due_date'],
        'is_urgent':task['is_urgent'],
    })
    return redirect(url_for('get_tasks'))


@app.route('/delete_task/<task_id>')
def delete_task(task_id):
    mongo.db.tasks.remove({'_id': ObjectId(task_id)})
    return redirect(url_for('get_tasks'))

@app.route('/get_categories')
def get_categories():
    return render_template('categories.html', categories = mongo.db.categories.find())

@app.route('/edit_category/<category_id>')
def edit_category(category_id):
    return render_template('editcategory.html',
    category = mongo.db.categories.find_one({'_id': ObjectId(category_id)})
    )

@app.route('/update_category/<category_id>', methods=['POST'])
def update_category(category_id):
    mongo.db.categories.update(
        {'_id': ObjectId(category_id)},
        {'category_name': request.form.get['category_name']}
        )
    return redirect(url_for('get_categories'))


@app.route('/delete_category/<category_id>')
def delete_category(category_id):
    mongo.db.categories.remove({'_id': ObjectId(category_id)})
    return render_template('categories.html', 
    categories = mongo.db.categories.find())





    
if __name__ == '__main__':
    app.run(
        host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True
        )