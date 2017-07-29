/**
 * Created by nicai on 2017/7/28.
 */
var ajax = function (method, path, data, callback) {
    var r = new XMLHttpRequest()
    r.open(method, path, true)
    r.setRequestHeader('Content-Type', 'application/json')
    r.onreadystatechange = function () {
        if (r.readyState == 4) {
            callback(r.response)
        }
    }
    r.send(data)
}

// 1, 往页面中添加输入框和提交按钮来增加 todo
//     添加页面元素
//     点击提交后, 发数据给 api, api如果成功, 则在页面中显示被创建的 todo
var insertInput = function () {
    var t = `
        <div>
            <input id="id-input-task">
            <button id="id-button-add" class='todo-add' data-action='todo_add'>add button</button>
        </div>
    `
    appendHtml(e('#id-div-todo-container'), t)
}

var insertCss = () => {
    var t = `
    <style>
        .todo-cell {
            outline: red 1px dashed;
        }
    </style>
    `
    // 注意, document.head 相当于 e('head')
    // document.head 和 document.body 是直接可以访问的元素
    // 因为这两个元素很特殊
    appendHtml(document.head, t)
}

var templateTodo = todo => {
    var task = todo.task
    var id = todo.id
    var t = `
        <div class='todo-cell' data-id='${id}'>
            <button class='todo-edit' data-action='todo_edit'>编辑</button>
            <button class='todo-delete' data-action='todo_delete'>删除</button>
            <span class='todo-task'>${task}</span>
        </div>
    `
    return t
}

var insertTodo = todo => {
    var container = e('#id-div-todo-container')
    var html = templateTodo(todo)
    appendHtml(container, html)
}

var insertTodos = todos => {
    for (var i = 0; i < todos.length; i++) {
        var todo = todos[i]
        insertTodo(todo)
    }
}

// 载入所有的 todos 并插入到页面中
var loadTodos = () => {
    var api = new Api()
    api.all(function (todos) {
        log('载入所有 todos', todos)
        insertTodos(todos)
    })
}

class Api {
    constructor(path) {
        this.baseUrl = 'locaohost:5000/' + path
    }

    get(path, callback) {
        var url = this.baseUrl + path
        ajax('GET', url, '', function (r) {
            var data = JSON.parse(r)
            callback(data)
        })
    }

    post(path, data, callback) {
        var url = this.baseUrl + path
        data = JSON.stringify(data)
        ajax('POST', url, data, function (r) {
            var data = JSON.parse(r)
            callback(data)
        })
    }

    all(callback) {
        var path = '/all'
        this.get(path, callback)
    }

    delete(id, callback) {
        var path = '/delete/' + id
        this.get(path, callback)
    }

    add(data, callback) {
        var path = '/add'
        this.post(path, data, callback)
    }

    update(id, data, callback) {
        var path = '/update/' + id
        this.post(path, data, callback)
    }
}

var actionAdd = event => {
    log('button click, add')
    var self = event.target
    // 获取 input 的输入
    var input = e('#id-input-task')
    var value = input.value
    // 组装成对象
    var data = {
        'task': value,
    }
    var api = new Api()
    api.add(data, function (todo) {
        log('创建成功', todo)
        // 往页面中插入被创建的 todo
        insertTodo(todo)
    })
}

var actionEdit = event => {
    log('button click, edit')
    // 找到 todo-task, 设置 contenteditable 属性, 并且让它获得焦点
    var self = event.target
    var todoCell = self.closest('.todo-cell')
    var task = todoCell.querySelector('.todo-task')
    task.contentEditable = true
    task.focus()
}

var actionDelete = event => {
    log('button click, delete')
    var self = event.target
    var todoCell = self.closest('.todo-cell')
    // 拿到 todo_id
    // 在事件中调用删除函数, 获取 todo_id 并且传给删除函数
    // 用 ajax 发送给服务器
    var todoId = todoCell.dataset.id
    var api = new Api()
    api.delete(todoId, function (todo) {
        log('删除成功', todo)
        // 删除后, 删除页面元素
        todoCell.remove()
    })
}

var actionUpdate = event => {
    log('按了回车键', event)
    var self = event.target
    // 取消事件的默认行为, 回车键在编辑标签内容的时候会默认断行
    event.preventDefault()
    // 取消 editable 状态, 发送 update 的请求
    self.contentEditable = false
    var todoCell = self.closest('.todo-cell')
    var todoId = todoCell.dataset.id
    // var url = 'https://vip.cocode.cc/sandbox/todo/3400711034/update/' + todoId
    var data = {
        'task': self.innerHTML,
    }
    var api = new Api()
    api.update(todoId, data, function (todo) {
        log('更新成功')
    })
}

var bindEventsDelegates = () => {
    // 声明所有可以处理的事件
    var actions = {
        todo_add: actionAdd,
        todo_delete: actionDelete,
        todo_edit: actionEdit,
    }
    // 绑定 add 按钮的事件委托
    var container = e('#id-div-todo-container')
    container.addEventListener('click', function (event) {
        var self = event.target
        var actionName = self.dataset.action
        var action = actions[actionName]
        if (action != undefined) {
            action(event)
        }
    })
}

var bindEventUpdate = () => {
    var container = e('#id-div-todo-container')
    // 绑定 keydown 事件, 当用户按键的时候被触发
    container.addEventListener('keydown', function (event) {
        var self = event.target
        if (self.classList.contains('todo-task')) {
            if (event.key == 'Enter') {
                actionUpdate(event)
            }
        }
    })
}

var bindEvents = () => {
    bindEventsDelegates()
    bindEventUpdate()
}

// 这是一个箭头函数
var __main = () => {
    // 初始化程序, 插入 input 标签和 css
    insertInput()
    insertCss()
    // 绑定事件委托
    bindEvents()
    // 载入所有 todos 并且在页面中显示
    loadTodos()
}

__main()