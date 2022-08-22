from flask_app import app
from flask import render_template, request, session, flash, redirect
from flask_app.models.message import Message
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/send_message', methods=['POST'])
def send_message():
    if 'id' not in session:
        return redirect('/')
    
    if not Message.validar_message(request.form):
        return redirect('/wall')

    Message.save(request.form)
    return redirect('/wall')

@app.route('/eliminar/mensaje/<int:id>') #Id del mensaje se recibe a través de URL
def eliminar_mensaje(id):
    if Message.validate_delete({'id':id, 'receiver_id': session['id']}):
        Message.destroy({'id': id})
    else:
        ip= request.remote_addr
        return render_template('danger.html', ip=ip, id=id)
    return redirect ('/wall')