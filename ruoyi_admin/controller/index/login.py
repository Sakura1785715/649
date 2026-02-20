
from ruoyi_common.base.model import  AjaxResponse
from ruoyi_common.domain.entity import SysUser
from ruoyi_common.domain.vo import LoginBody
from ruoyi_common.descriptor.serializer import JsonSerializer
from ruoyi_common.descriptor.validator import BodyValidator
from ruoyi_common.utils import security_util as SecurityUtil
from ruoyi_common.constant import Constants
from ruoyi_system.service import SysMenuService
from ruoyi_framework.service import LoginService,SysPermissionService
from ... import reg
from pydantic import BaseModel
from ruoyi_admin.ext import fredis
from ruoyi_system.service.sys_user import SysUserService

@reg.api.route("/login", methods=["POST"])
@BodyValidator()
@JsonSerializer()
def index_login(dto:LoginBody):
    '''
        登录接口
    '''
    token = LoginService.login(dto)
    ajax_response = AjaxResponse.from_success()
    setattr(ajax_response, Constants.TOKEN, token)
    return ajax_response


@reg.api.route("/getInfo", methods=["GET"])
@JsonSerializer()
def index_get_info():
    '''
        获取用户信息接口
    '''
    user:SysUser = SecurityUtil.get_login_user().user
    roles = SysPermissionService.get_role_permission(user)
    perms = SysPermissionService.get_menu_permission(user)
    ajax_response = AjaxResponse.from_success()
    setattr(ajax_response, "roles", list(roles))
    setattr(ajax_response, "permissions", list(perms))
    setattr(ajax_response, "user", user.model_dump())
    return ajax_response


@reg.api.route("/getRouters", methods=["GET"])
@JsonSerializer()
def index_get_routers():
    '''
        获取路由信息接口
    '''
    user_id = SecurityUtil.get_user_id()
    menus = SysMenuService.select_menu_tree_by_user_id(user_id)
    ajax_response = AjaxResponse.from_success(
        data=SysMenuService.build_menus(menus)
    )
    return ajax_response


@reg.api.route("/logout", methods=["POST"])
@JsonSerializer()
def index_logout():
    '''
        登出接口
    '''
    flag = LoginService.logout()
    return AjaxResponse.from_success(msg="登出成功") \
        if flag else AjaxResponse.from_error(msg="登出异常")



class ResetPwdBody(BaseModel):
    username: str
    newPassword: str
    code: str
    uuid: str = ""

@reg.api.route("/resetPwd", methods=["POST"])
@BodyValidator()
@JsonSerializer()
def reset_pwd(dto: ResetPwdBody):
    '''
        忘记密码：校验验证码并重置密码接口
    '''
    verify_key = getattr(Constants, 'CAPTCHA_CODE_KEY', 'captcha_codes:') + dto.uuid
    captcha = fredis.get(verify_key)
    
    if not captcha:
        return AjaxResponse.from_error(msg="验证码已失效，请重新获取")
        
    fredis.delete(verify_key)
    
    if captcha.decode('utf-8').lower() != dto.code.lower():
        return AjaxResponse.from_error(msg="验证码错误")

    user = SysUserService.select_user_by_user_name(dto.username)
    if not user:
        return AjaxResponse.from_error(msg="该工号不存在，请核对后重新输入")

    # 更新密码并保存到数据库 
    user.password = dto.newPassword
    success = SysUserService.reset_pwd(user)
    
    if success:
        return AjaxResponse.from_success(msg="密码重置成功")
    else:
        return AjaxResponse.from_error(msg="密码重置失败，请联系系统管理员")