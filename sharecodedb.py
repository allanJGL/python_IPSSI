#!/usr/bin/env python3

from flask import Flask, request, render_template, \
    redirect

from model_sqlite import save_info, \
    read_code, \
    read_lang, \
    edit_info, \
    get_last_entries_from_files

app = Flask(__name__)


@app.route('/')
def index():
    # d = { 'last_added':[ { 'uid':'testuid', 'code':'testcode' } ] }
    d = {'last_added': get_last_entries_from_files()}
    return render_template('index.html', **d)


@app.route('/create')
def create():
    uid = save_info()
    return redirect("{}edit/{}".format(request.host_url, uid))


@app.route('/edit/<string:uid>/')
def edit(uid):
    code = read_code(uid)
    lang = read_lang(uid)
    if code is None:
        return render_template('error.html', uid=uid)
    d = dict(uid=uid, code=code, lang=lang,
             url="{}view/{}".format(request.host_url, uid))
    return render_template('edit.html', **d)


@app.route('/publish', methods=['POST'])
def publish():
    code = request.form['code']
    uid = request.form['uid']
    lang = request.form['lang']
    edit_info(uid, code, lang)
    return redirect("{}{}/{}".format(request.host_url,
                                     request.form['submit'],
                                     uid))


@app.route('/view/<string:uid>/')
def view(uid):
    code = read_code(uid)
    lang = read_lang(uid)
    if code is None:
        return render_template('error.html', uid=uid)
    if lang is None:
        lang = ''
    d = dict(uid=uid, code=code, lang=lang,
             url="{}view/{}".format(request.host_url, uid))
    return render_template('view.html', **d)


@app.route('/admin/')
def admin():
    pass


if __name__ == '__main__':
    app.run()
