# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, current_app, Blueprint
from flask_bootstrap import Bootstrap
import os
from PIL import Image
upload_blue = Blueprint(__name__, 'upload')




def new_name(shuffix, length=32):
    import string, random
    myStr = string.ascii_letters + '0123456789'
    newName = ''.join(random.choice(myStr) for i in range(length))
    return newName + shuffix


def allowed_file(shuffix):
    return shuffix in current_app.config['ALLOWED_EXTENSIONS']


@upload_blue.route('/upload', methods=['GET', 'POST'])
def upload():
    img_name = None
    if request.method == 'POST':
        file = request.files.get('file')  # 拿到文件对象
        filename = file.filename  # 获取上传的图片名称
        shuffix = os.path.splitext(filename)[-1]
        if allowed_file(shuffix):
            newName = new_name(shuffix)
            img_name = newName
            # 拼凑完整的图片上传路径
            newPath = os.path.join(app.config['UPLOAD_FOLDER'], newName)
            file.save(newPath)  # 保存图片

            # 处理图片的缩放
            img = Image.open(newPath)
            print(img.size)
            # 重新设置大小和尺寸
            img.thumbnail((200, 200))
            img.save(newPath)
    return render_template('upload.html', newName=img_name)



def register_blue(app):
    app.register_blueprint(upload_blue, )

if __name__ == '__main__':
    manager.run()
