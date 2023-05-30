import datetime
import os
os.system("pip install --upgrade paddlenlp")

import shutil
import numpy as np
import pandas as pd
import re
import json
from tqdm import tqdm
from paddlenlp import Taskflow
from docx import Document
from docx.shared import Inches
import streamlit as st

st.header("图片格式简历识别")
schema = st.multiselect(
    '抽取实体信息',
    ['姓名', '出生年月', '电话', '性别', '项目名称', '项目责任', '项目时间', '籍贯', '政治面貌', '落户市县', '毕业院校', '学位', '毕业时间', '工作时间', '工作内容', '职务', '工作单位'],
    ['姓名', '出生年月', '电话', '性别', '籍贯', '政治面貌', '落户市县', '毕业院校', '学位', '毕业时间'])
per_image = st.file_uploader("上传图片", type=['png', 'jpg'], label_visibility='hidden')
if per_image:
    from io import BytesIO
    from PIL import Image
    st.image(per_image)
    # To read file as bytes:
    bytes_data = per_image.getvalue()
    #将字节数据转化成字节流
    bytes_data = BytesIO(bytes_data)
    #Image.open()可以读字节流
    capture_img = Image.open(bytes_data)
    capture_img = capture_img.convert('RGB')
    capture_img.save('temp.jpeg', quality=95)
else:
    st.image("temp.jpeg")
test=st.button("提交图片")
if test:
    my_ie = Taskflow("information_extraction", schema=schema, task_path='PaddleNLP/applications/information_extraction/text/checkpoint/model_best')
    a = my_ie({"doc":'temp.jpeg'})
    for i in schema:
        if i in a[0]:
            st.write(i + "：" + a[0][i][0]['text'])
