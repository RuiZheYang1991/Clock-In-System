from api.mysql.controllers.controller import EmployeeAPI, EarlyClockIn
from api.utils.admin_helpers import validate_email

from flask_admin import Admin, AdminIndexView, BaseView, expose
from flask import redirect, url_for, request
# from flask_security import current_user
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user


from flask_security.forms import LoginForm as OriginalLoginForm
from wtforms import validators




class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login', next=request.url))
    # def is_accessible(self):
    #     return current_user.is_authenticated and current_user.has_role('admin')
    #
    # def inaccessible_callback(self, name, **kwargs):
    #     return redirect(url_for('security.login', next=request.url))
# views_bp = Blueprint('views', __name__)
# You can customize this class as you like
class EmployeeModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login', next=request.url))
    # def is_accessible(self):
    #     return current_user.is_authenticated and current_user.has_role('admin')
    # def inaccessible_callback(self, name, **kwargs):
    #     return redirect(url_for('security.login', next=request.url))
    column_labels = {
        'name' : '姓名',
        'email' : '電子郵件',
        'position' : '職稱',
        'employee_number' : '員工號碼',
        'create_at' : '到職日',
        'phone_number' :'電話號碼',
        'gender' :'性別',
        'department' :'部門',
        'birth_date':'出生年月日',
        'address' : '住址',
        'salary' : '薪資',
        'nationality' : '國籍'
    }
    form_excluded_columns = ['create_at']
    # 顯示在列表視圖中的字段
    column_list = ('employee_number','name', 'email','phone_number','gender','birth_date', 'position','department','address','nationality','create_at')
    column_editable_list = ('name', 'email', 'position')
    # 可以搜索的字段
    column_searchable_list = ('employee_number','name', 'email')

    # 可以過濾的字段
    column_filters = ('position',)
    form_args = {
        'email': {
            'validators': [validate_email],
        }
    }
    form_choices = {
        'gender': [
            ('male', '男'),
            ('female', '女')
        ],
        'department': [
            ('HR', '人力資源'),
            ('Engineering', '工程'),
            ('Marketing', '市場營銷'),
            # 更多部門
        ],
        'nationality': [
            ('US', '美國'),
            ('UK', '英國'),
            ('CN', '中國'),
            ('TW', '台灣'),
            ('other', '其他'),
            # ... 其他國籍
        ]
    }
    column_descriptions = {
        'email': '用於登錄和接收通知的電子郵件地址。',
        'salary': '月薪。'
    }
    column_sortable_list = ('employee_number', 'name', 'email', 'create_at')

    column_formatters = {
        'birth_date': lambda v, c, m, p: m.birth_date.strftime('%Y-%m-%d') if m.birth_date else '',
    }




class EmployeeRecordView(BaseView):
    @expose('/')
    def index(self):
        api = EmployeeAPI()
        employee_data = api.get()
        return self.render('admin/employee_record.html', employee_data=employee_data)

class EarlyClockView(BaseView):
    @expose('/')
    def index(self):
        api = EarlyClockIn()
        clock_data = api.get()
        return self.render('admin/early_clock.html', clock_data=clock_data)

# column_labels：用於自訂欄位標籤的顯示。您可以使用這個屬性來替換欄位名稱為更加易讀的標籤。
#
# column_editable_list：用於指定哪些欄位可以在列表頁面中直接編輯。將欄位名稱添加到這個列表中，將使它們在列表頁面中變成可編輯的欄位。
#
# column_searchable_list：用於指定可以進行搜尋的欄位。將欄位名稱添加到這個列表中，將允許您在列表頁面上使用搜索框來搜尋這些欄位的內容。
#
# column_sortable_list：用於指定可以進行排序的欄位。將欄位名稱添加到這個列表中，將允許您在列表頁面上按這些欄位進行排序。
#
# column_default_sort：用於設定預設的排序方式。可以設定為元組，包含要排序的欄位名稱和排序順序（'asc' 或 'desc'）。
#
# column_formatters：用於自訂欄位在列表頁面中的顯示格式。可以使用這個屬性來對特定欄位的值進行格式化處理。
#
# column_descriptions：用於提供欄位的描述信息，將顯示為欄位標籤的 tooltip。
#
# form_columns：用於指定在新增和編輯頁面中顯示的欄位。默認情況下，所有欄位都會顯示，但您可以使用這個屬性僅顯示特定的欄位。
#
# column_choices：用於定義欄位的選項列表，使它們在列表頁面中以人類可讀的值顯示。
# @views_bp.route('/')
# def index():
#     return render_template('indexbak.html')
