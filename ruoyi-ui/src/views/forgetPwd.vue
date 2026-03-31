<template>
    <div class="login-container">
      <div class="login-left">
        <div class="train-bg-wrapper">
          <svg class="train-line-art" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="0.5">
            <path d="M21 21H3V11.2C3 6.671 6.671 3 11.2 3H12.8C17.329 3 21 6.671 21 11.2V21Z"></path>
            <path d="M3 15H21"></path><path d="M9 21V23"></path><path d="M15 21V23"></path><path d="M3 11H21"></path>
            <circle cx="7" cy="18" r="1.5"></circle><circle cx="17" cy="18" r="1.5"></circle><path d="M8 7H16"></path>
          </svg>
        </div> 
  
        <div class="brand-content">
          <div class="brand-line"></div>
          <h1 class="brand-title">高铁列控设备<br>故障预测与<br>健康管理系统</h1>
          <div class="brand-subtitle-box">
            <p class="brand-subtitle">High-Speed Train <br> PHM System V1.0</p>
          </div>
        </div>
        <div class="system-id">SYSTEM_ID: CRH_PHM_PROD_01</div>
      </div>
  
      <div class="login-right">
        <div class="login-content-wrapper">
          <div class="form-header">
            <h2 class="form-title">Password Reset</h2>
            <p class="form-subtitle">Verify your identity to reset system access.</p>
          </div>
  
          <el-form ref="resetForm" :model="resetForm" :rules="resetRules" class="login-form">
            <el-form-item prop="username">
              <label class="input-label">EMPLOYEE ID / 工号</label>
              <el-input v-model="resetForm.username" type="text" auto-complete="off" placeholder="Enter your ID">
                <i slot="prefix" class="el-icon-postcard input-icon"></i>
              </el-input>
            </el-form-item>
  
            <div class="captcha-row" v-if="captchaOnOff">
               <el-form-item prop="code" class="captcha-input-item">
                <label class="input-label">VERIFICATION / 验证码</label>
                <el-input v-model="resetForm.code" auto-complete="off" placeholder="Code">
                  <i slot="prefix" class="el-icon-key input-icon"></i>
                </el-input>
              </el-form-item>
              
              <div class="captcha-img-box" title="点击刷新验证码">
                 <img :src="codeUrl" @click="getCode" class="login-code-img" v-if="codeUrl"/>
                 <div v-else class="captcha-placeholder" @click="getCode">8X2A</div>
              </div>
            </div>
  
            <el-form-item prop="newPassword">
              <label class="input-label">NEW PASSWORD / 新密码</label>
              <el-input v-model="resetForm.newPassword" type="password" auto-complete="off" placeholder="••••••••">
                <i slot="prefix" class="el-icon-lock input-icon"></i>
              </el-input>
            </el-form-item>
  
            <el-form-item prop="confirmPassword">
              <label class="input-label">CONFIRM PASSWORD / 确认新密码</label>
              <el-input v-model="resetForm.confirmPassword" type="password" auto-complete="off" placeholder="••••••••" @keyup.enter.native="handleReset">
                <i slot="prefix" class="el-icon-circle-check input-icon"></i>
              </el-input>
            </el-form-item>
  
            <el-form-item style="width:100%; margin-top: 2rem;">
              <el-button :loading="loading" size="medium" type="primary" class="login-btn" @click.native.prevent="handleReset">
                <span v-if="!loading">重置密码 / Reset Password</span>
                <span v-else>处理中...</span>
                <i class="el-icon-refresh-right ml-2" v-if="!loading"></i>
              </el-button>
            </el-form-item>
  
            <div class="remember-row" style="justify-content: center; margin-top: 1rem;">
              <a href="#" class="forgot-link" @click.prevent="goBack">
                <i class="el-icon-back"></i> Back to Login / 返回登录
              </a>
            </div>
          </el-form>
  
          <div class="form-footer">
            <div class="footer-lock">
              <i class="el-icon-lock"></i>
              <span>AUTHORIZED PERSONNEL ONLY</span>
            </div>
            <p class="footer-note">Protected by Industrial Security Protocols • Internal System Access</p>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  // 直接复用若依现成的获取验证码接口
  import { getCodeImg, resetPwd } from '@/api/login'
  
  export default {
    name: 'ForgetPwd',
    data() {
      // 需求2：自定义的密码一致性校验逻辑
      const validateConfirmPassword = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请再次输入密码'));
        } else if (value !== this.resetForm.newPassword) {
          callback(new Error('两次输入的密码不一致!'));
        } else {
          callback();
        }
      };
  
      return {
        codeUrl: '', // 存储验证码图片
        resetForm: {
          username: '',
          code: '',
          uuid: '', // 提交给后端校验所需的uuid
          newPassword: '',
          confirmPassword: '' // 绑定的确认密码字段
        },
        resetRules: {
          username: [{ required: true, trigger: 'blur', message: '请输入您的工号' }],
          code: [{ required: true, trigger: 'change', message: '请输入验证码' }],
          newPassword: [
            { required: true, trigger: 'blur', message: '请输入新密码' },
            { min: 5, max: 20, message: '长度在 5 到 20 个字符', trigger: 'blur' }
          ],
          // 应用自定义校验规则
          confirmPassword: [
            { required: true, trigger: 'blur', validator: validateConfirmPassword }
          ]
        },
        loading: false,
        captchaOnOff: true 
      }
    },
    created() {
      // 页面加载时自动获取一次图形验证码
      this.getCode();
    },
    methods: {
      // 需求1：获取验证码逻辑（复刻 login.vue）
      getCode() {
        getCodeImg().then(res => {
          this.captchaOnOff = res.captchaOnOff === undefined ? true : res.captchaOnOff;
          if (this.captchaOnOff) {
            this.codeUrl = 'data:image/gif;base64,' + res.img;
            this.resetForm.uuid = res.uuid;
          }
        });
      },
      handleReset() {
      this.$refs.resetForm.validate(valid => {
        if (valid) {
          this.loading = true;
          // 调用刚刚封装的后端接口
          resetPwd({
            username: this.resetForm.username,
            newPassword: this.resetForm.newPassword,
            code: this.resetForm.code,
            uuid: this.resetForm.uuid
          }).then(res => {
            this.loading = false;
            // 成功后给予工业级提示，并延迟跳转回登录页
            this.$message({
              message: '密码重置成功！安全凭证已更新，即将返回登录大厅...',
              type: 'success',
              duration: 2000
            });
            setTimeout(() => {
              this.$router.push('/login');
            }, 2000);
          }).catch(err => {
            // 如果报错（比如验证码错误/工号不存在），停止 loading 并刷新验证码
            this.loading = false;
            this.getCode(); 
          });
        } else {
          this.$message.error("请正确填写所有标红的安全校验信息");
          return false;
        }
      });
    },
      goBack() {
        this.$router.push('/login');
      }
    }
  }
  </script>
  
  <style rel="stylesheet/scss" lang="scss" scoped>
  $phm-dark: #111A35;
  $primary: #2563EB;
  $text-dark: #0F172A;
  $text-gray: #64748B;
  $border-light: #E2E8F0;
  $input-bg: #FFFFFF;
  
  .login-container { display: flex; height: 100vh; width: 100%; font-family: 'Inter', 'Noto Sans SC', sans-serif; overflow: hidden; }
  
  .login-left {
    display: none; @media (min-width: 768px) { display: flex; width: 40%; }
    position: relative; background-color: $phm-dark; flex-direction: column; justify-content: center; align-items: center; padding: 3rem; overflow: hidden;
    .train-bg-wrapper {
      position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; pointer-events: none; z-index: 0;
      .train-line-art { width: 150%; height: auto; color: white; opacity: 0.1; transform: rotate(-12deg) translate(2.5rem, 5rem); mask-image: linear-gradient(to bottom, rgba(0,0,0,1) 50%, rgba(0,0,0,0)); -webkit-mask-image: linear-gradient(to bottom, rgba(0,0,0,1) 50%, rgba(0,0,0,0)); }
    }
    .brand-content { position: relative; z-index: 10; width: 100%; max-width: 440px; text-align: left;
      .brand-line { width: 4rem; height: 4px; background-color: $primary; margin-bottom: 1.5rem; }
      .brand-title { font-size: 2.5rem; font-weight: 700; color: white; line-height: 1.2; margin-bottom: 1.5rem; letter-spacing: 0.05em; }
      .brand-subtitle-box { border-left: 2px solid $primary; padding-left: 1rem; .brand-subtitle { color: rgba(191, 219, 254, 0.8); font-size: 1.25rem; font-weight: 300; letter-spacing: 0.1em; line-height: 1.4; } }
    }
    .system-id { position: absolute; bottom: 2rem; left: 3rem; color: rgba(96, 165, 250, 0.3); font-family: monospace; font-size: 0.75rem; letter-spacing: 0.2em; z-index: 10; }
  }
  
  .login-right {
    flex: 1; display: flex; align-items: center; justify-content: center; background-color: white; padding: 1.5rem;
    .login-content-wrapper { width: 100%; max-width: 440px; }
    .form-header { text-align: left; margin-bottom: 2rem; .form-title { font-size: 1.5rem; font-weight: 700; color: $text-dark; margin-bottom: 0.5rem; } .form-subtitle { color: $text-gray; font-size: 0.875rem; } }
    
    .login-form {
      .el-form-item { margin-bottom: 1.25rem; }
      .input-label { display: block; font-size: 0.75rem; font-weight: 600; color: #475569; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.375rem; margin-left: 0.25rem; }
      
      ::v-deep .el-input__inner { height: 48px; line-height: 48px; padding-left: 44px; background-color: white; border: 1px solid $border-light; border-radius: 0.25rem; color: $text-dark; font-weight: 500; transition: all 0.2s; &:focus { border-color: $primary; box-shadow: 0 0 0 1px $primary; } &::placeholder { color: #94a3b8; } }
      ::v-deep .el-input__prefix { left: 12px; display: flex; align-items: center; }
      .input-icon { font-size: 20px; color: #94a3b8; }
      ::v-deep .el-input__inner:focus + .el-input__prefix .input-icon, ::v-deep .el-input__inner:focus ~ .el-input__prefix .input-icon { color: $primary; }
    }
  
    // 完全复刻图片验证码样式
    .captcha-row {
      display: flex; align-items: flex-end; gap: 0.75rem; width: 100%;
      .captcha-input-item { flex: 1; margin-bottom: 0; ::v-deep .el-form-item__content { line-height: normal; } }
      .captcha-img-box {
        width: 128px; height: 48px; background-color: #F1F5F9; border: 1px solid $border-light; border-radius: 0.25rem; display: flex; align-items: center; justify-content: center; cursor: pointer; position: relative; overflow: hidden; flex-shrink: 0;
        &::before { content: ''; position: absolute; inset: 0; opacity: 0.1; background-image: repeating-linear-gradient(45deg, #000 0, #000 1px, transparent 0, transparent 50%); background-size: 10px 10px; }
        img { width: 100%; height: 100%; object-fit: cover; position: relative; z-index: 2; }
        .captcha-placeholder { font-family: monospace; font-size: 1.125rem; font-weight: 700; color: #475569; letter-spacing: 0.2em; font-style: italic; z-index: 2; }
      }
    }
  
    .remember-row { display: flex; justify-content: space-between; align-items: center; margin-top: 0.5rem; margin-bottom: 1.5rem; .forgot-link { font-size: 0.875rem; color: $text-gray; font-weight: 500; text-decoration: none; transition: color 0.2s; &:hover { color: $primary; } } }
    .login-btn { width: 100%; height: 52px; background-color: $primary; border-color: $primary; font-size: 1rem; font-weight: 600; letter-spacing: 0.025em; border-radius: 0.375rem; &:hover { background-color: darken($primary, 5%); transform: translateY(-1px); } }
    
    .form-footer { margin-top: 3rem; width: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center; .footer-lock { display: flex; align-items: center; justify-content: center; gap: 0.5rem; color: #94a3b8; margin-bottom: 0.5rem; i { font-size: 1rem; } span { font-size: 0.75rem; font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase; } } .footer-note { font-size: 0.625rem; color: #cbd5e1; text-align: center; } }
  }
  </style>