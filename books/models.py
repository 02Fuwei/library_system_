from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # library_id（图书馆编号）: 用于唯一标识图书馆系统中的每个用户。
    library_id = models.CharField(max_length=128, unique=True)
    # address（地址）: 用户的家庭地址或通信地址。
    address = models.TextField()
    # phone_number（电话号码）: 用户的联系电话。
    phone_number = models.CharField(max_length=15)
    # membership_type（会员类型）: 标识用户是普通会员还是特殊会员（例如学生、教师或退休人员）。
    membership_type = models.IntegerField(default=0)  # 0代表用户，1代表管理员
    # Membership Expiry Date（会员到期日期）: 会员资格的到期日期，用于管理用户的会员续订。
    membership_expiry = models.DateField(default=timezone.now() + timedelta(days=365))
    # Loan Limit（借书限额）: 用户可以借阅的最大书籍数量。
    loan_limit = models.IntegerField(default=5)
    # Fines（罚款）: 用户当前的罚款总额，通常是由于逾期未还书籍产生。
    fines = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

