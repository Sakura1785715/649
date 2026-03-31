<template>
  <div class="login-container">
    <div class="login-left">
      <div class="train-bg-wrapper">
        <svg
          class="train-line-art"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="0.5"
        >
          <path d="M21 21H3V11.2C3 6.671 6.671 3 11.2 3H12.8C17.329 3 21 6.671 21 11.2V21Z"></path>
          <path d="M3 15H21"></path>
          <path d="M9 21V23"></path>
          <path d="M15 21V23"></path>
          <path d="M3 11H21"></path>
          <circle cx="7" cy="18" r="1.5"></circle>
          <circle cx="17" cy="18" r="1.5"></circle>
          <path d="M8 7H16"></path>
        </svg>
      </div> 

      <div class="brand-content">
        <div class="brand-line"></div>
        
        <h1 class="brand-title">
          高铁列控设备<br>故障预测与<br>健康管理系统
        </h1>
        
        <div class="brand-subtitle-box">
          <p class="brand-subtitle">
            High-Speed Train <br> PHM System V1.0
          </p>
        </div>
      </div>

      <div class="system-id">SYSTEM_ID: CRH_PHM_PROD_01</div>
    </div>

    <div class="login-right">
      <div class="login-content-wrapper">
        <div class="form-header">
          <h2 class="form-title">Secure Login</h2>
          <p class="form-subtitle">Please identify yourself to access the secure terminal.</p>
        </div>

        <el-form ref="loginForm" :model="loginForm" :rules="loginRules" class="login-form">
          <el-form-item prop="username">
            <label class="input-label">EMPLOYEE ID / 工号</label>
            <el-input
              v-model="loginForm.username"
              type="text"
              auto-complete="off"
              placeholder="Enter your ID"
            >
              <i slot="prefix" class="el-icon-postcard input-icon"></i>
            </el-input>
          </el-form-item>

          <el-form-item prop="password">
            <label class="input-label">PASSWORD / 密码</label>
            <el-input
              v-model="loginForm.password"
              type="password"
              auto-complete="off"
              placeholder="••••••••"
              @keyup.enter.native="handleLogin"
            >
              <i slot="prefix" class="el-icon-lock input-icon"></i>
            </el-input>
          </el-form-item>

          <div class="captcha-row">
             <el-form-item prop="code" class="captcha-input-item">
              <label class="input-label">VERIFICATION / 验证码</label>
              <el-input
                v-model="loginForm.code"
                auto-complete="off"
                placeholder="Code"
                @keyup.enter.native="handleLogin"
              >
                <i slot="prefix" class="el-icon-key input-icon"></i>
              </el-input>
            </el-form-item>
            
            <div class="captcha-img-box" title="点击刷新验证码">
               <img :src="codeUrl" @click="getCode" class="login-code-img" v-if="codeUrl"/>
               <div v-else class="captcha-placeholder" @click="getCode">8X2A</div>
            </div>
          </div>

          <div class="remember-row">
            <el-checkbox v-model="loginForm.rememberMe">Remember ID</el-checkbox>
            <a href="#" class="forgot-link" @click.prevent="handleForgetPwd">Forgot Password?</a>
          </div>

          <el-form-item style="width:100%;">
            <el-button
              :loading="loading"
              size="medium"
              type="primary"
              class="login-btn"
              @click.native.prevent="handleLogin"
            >
              <span v-if="!loading">登录 / Login</span>
              <span v-else>登录中...</span>
              <i class="el-icon-right ml-2"></i>
            </el-button>
          </el-form-item>
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
import { getCodeImg } from '@/api/login'
import Cookies from 'js-cookie'
import { encrypt, decrypt } from '@/utils/jsencrypt'

export default {
  name: 'Login',
  data() {
    return {
      codeUrl: '',
      loginForm: {
        username: 'admin',
        password: 'admin123',
        rememberMe: false,
        code: '',
        uuid: ''
      },
      loginRules: {
        username: [
          { required: true, trigger: 'blur', message: '请输入您的账号' }
        ],
        password: [
          { required: true, trigger: 'blur', message: '请输入您的密码' }
        ],
        code: [{ required: true, trigger: 'change', message: '请输入验证码' }]
      },
      loading: false,
      captchaOnOff: true, 
      redirect: undefined
    }
  },
  watch: {
    $route: {
      handler: function(route) {
        this.redirect = route.query && route.query.redirect
      },
      immediate: true
    }
  },
  created() {
    this.getCode()
    this.getCookie()
  },
  methods: {
    getCode() {
      getCodeImg().then(res => {
        this.captchaOnOff = res.captchaOnOff === undefined ? true : res.captchaOnOff
        if (this.captchaOnOff) {
          this.codeUrl = 'data:image/gif;base64,' + res.img
          this.loginForm.uuid = res.uuid
        }
      })
    },
    handleForgetPwd() {
      // alert("探针测试：按钮点击事件已成功触发！");
      // console.log("---- 准备跳转路由 ----");
      this.$router.push('/forgetPwd');
    },
    getCookie() {
      const username = Cookies.get('username')
      const password = Cookies.get('password')
      const rememberMe = Cookies.get('rememberMe')
      this.loginForm = {
        username: username === undefined ? this.loginForm.username : username,
        password: password === undefined ? this.loginForm.password : decrypt(password),
        rememberMe: rememberMe === undefined ? false : Boolean(rememberMe)
      }
    },
    handleLogin() {
      this.$refs.loginForm.validate(valid => {
        if (valid) {
          this.loading = true
          if (this.loginForm.rememberMe) {
            Cookies.set('username', this.loginForm.username, { expires: 30 })
            Cookies.set('password', encrypt(this.loginForm.password), { expires: 30 })
            Cookies.set('rememberMe', this.loginForm.rememberMe, { expires: 30 })
          } else {
            Cookies.remove('username')
            Cookies.remove('password')
            Cookies.remove('rememberMe')
          }
          this.$store.dispatch('Login', this.loginForm).then(() => {
            this.$router.push({ path: this.redirect || '/' }).catch(() => {})
          }).catch(() => {
            this.loading = false
            if (this.captchaOnOff) {
              this.getCode()
            }
          })
        }
      })
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
// 1. 提取参考图中的核心色值
$phm-dark: #111A35;       // 左侧深蓝背景
$primary: #2563EB;        // 工业蓝 (按钮/高亮)
$text-dark: #0F172A;      // 标题黑
$text-gray: #64748B;      // 说明灰
$border-light: #E2E8F0;   // 浅灰边框
$input-bg: #FFFFFF;       // 输入框背景

.login-container {
  display: flex;
  height: 100vh;
  width: 100%;
  font-family: 'Inter', 'Noto Sans SC', sans-serif; // 使用参考图字体
  overflow: hidden;
}

// =========================================
// 左侧区域 (修复重点)
// =========================================
.login-left {
  display: none; 
  @media (min-width: 768px) {
    display: flex;
    width: 40%; // 参考图左侧较窄，约40%
  }
  position: relative;
  background-color: $phm-dark;
  flex-direction: column;
  justify-content: center; // 垂直居中
  align-items: center;     // 水平居中
  padding: 3rem;
  overflow: hidden;

  // --- 1. 小火车背景修复 ---
  .train-bg-wrapper {
    position: absolute;
    inset: 0; // top/left/right/bottom: 0
    display: flex;
    align-items: center;
    justify-content: center;
    pointer-events: none;
    z-index: 0; // 放在最底层

    .train-line-art {
      width: 150%;  // 放大到150%
      height: auto;
      color: white;
      opacity: 0.1; // 降低透明度
      // 核心：旋转和位移，复刻参考图角度
      transform: rotate(-12deg) translate(2.5rem, 5rem); 
      // 核心：渐变遮罩，让底部渐隐
      mask-image: linear-gradient(to bottom, rgba(0,0,0,1) 50%, rgba(0,0,0,0));
      -webkit-mask-image: linear-gradient(to bottom, rgba(0,0,0,1) 50%, rgba(0,0,0,0));
    }
  }

  // --- 2. 品牌文字内容 ---
  .brand-content {
    position: relative;
    z-index: 10;
    width: 100%;
    max-width: 440px;
    text-align: left;
    
    .brand-line {
      width: 4rem;
      height: 4px;
      background-color: $primary;
      margin-bottom: 1.5rem;
    }

    .brand-title {
      font-size: 2.5rem; // 对应 text-4xl
      font-weight: 700;
      color: white;
      line-height: 1.2;
      margin-bottom: 1.5rem;
      letter-spacing: 0.05em;
    }

    .brand-subtitle-box {
      border-left: 2px solid $primary;
      padding-left: 1rem;
      
      .brand-subtitle {
        color: rgba(191, 219, 254, 0.8); // blue-200/80
        font-size: 1.25rem;
        font-weight: 300;
        letter-spacing: 0.1em;
        line-height: 1.4;
      }
    }
  }

  // --- 3. 底部 System ID ---
  .system-id {
    position: absolute;
    bottom: 2rem;
    left: 3rem;
    color: rgba(96, 165, 250, 0.3); // extremely subtle blue
    font-family: monospace;
    font-size: 0.75rem;
    letter-spacing: 0.2em;
    z-index: 10;
  }
}

// =========================================
// 右侧区域 (工业风表单)
// =========================================
.login-right {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: white;
  padding: 1.5rem;

  .login-content-wrapper {
    width: 100%;
    max-width: 440px;
  }

  .form-header {
    text-align: left; // 参考图是左对齐的
    margin-bottom: 2rem;

    .form-title {
      font-size: 1.5rem;
      font-weight: 700;
      color: $text-dark;
      margin-bottom: 0.5rem;
    }
    .form-subtitle {
      color: $text-gray;
      font-size: 0.875rem;
    }
  }

  .login-form {
    .el-form-item {
      margin-bottom: 1.25rem;
    }

    // 标签样式复刻：全大写、灰色、小字体
    .input-label {
      display: block;
      font-size: 0.75rem; // xs
      font-weight: 600;
      color: #475569; // slate-600
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 0.375rem;
      margin-left: 0.25rem;
    }

    // --- 深度定制 Element Input ---
    ::v-deep .el-input__inner {
      height: 48px;
      line-height: 48px;
      padding-left: 44px; // 为图标留空间
      background-color: white;
      border: 1px solid $border-light;
      border-radius: 0.25rem; // sm radius (2px-4px)
      color: $text-dark;
      font-weight: 500;
      transition: all 0.2s;

      &:focus {
        border-color: $primary;
        box-shadow: 0 0 0 1px $primary; // Ring effect
      }
      
      &::placeholder {
        color: #94a3b8;
      }
    }

    // 图标样式
    ::v-deep .el-input__prefix {
      left: 12px;
      display: flex;
      align-items: center;
    }
    .input-icon {
      font-size: 20px;
      color: #94a3b8;
    }
    // 当输入框focus时，图标变色
    ::v-deep .el-input__inner:focus + .el-input__prefix .input-icon,
    ::v-deep .el-input__inner:focus ~ .el-input__prefix .input-icon {
      color: $primary;
    }
  }

  // 验证码行
  .captcha-row {
    display: flex;
    align-items: flex-end; // 关键修复：强制底部对齐。这样图片会自动对齐到输入框，而不是标签。
    gap: 0.75rem;
    width: 100%;
    
    .captcha-input-item {
      flex: 1;
      margin-bottom: 0; // 消除 Element UI 可能自带的底部边距干扰
      
      // 确保 input 内部没有额外的行高干扰
      ::v-deep .el-form-item__content {
         line-height: normal; 
      }
    }

    .captcha-img-box {
      // 移除之前的 margin-top Hack，改用 Flex 底部对齐
      // margin-top: 1.4rem;  <-- 删除这行
      
      width: 128px;
      height: 48px; // 必须严格等于 el-input__inner 的高度
      background-color: #F1F5F9; 
      border: 1px solid $border-light;
      border-radius: 0.25rem;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      position: relative;
      overflow: hidden;
      flex-shrink: 0; // 防止被挤压

      // 模拟斜线背景
      &::before {
        content: '';
        position: absolute;
        inset: 0;
        opacity: 0.1;
        background-image: repeating-linear-gradient(
          45deg,
          #000 0,
          #000 1px,
          transparent 0,
          transparent 50%
        );
        background-size: 10px 10px;
      }
      
      img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        position: relative;
        z-index: 2;
      }
      
      .captcha-placeholder {
        font-family: monospace;
        font-size: 1.125rem;
        font-weight: 700;
        color: #475569;
        letter-spacing: 0.2em;
        font-style: italic;
        z-index: 2;
      }
    }
  }

  // 记住密码行
  .remember-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 0.5rem;
    margin-bottom: 1.5rem;

    ::v-deep .el-checkbox__label {
      font-size: 0.875rem;
      color: #475569;
    }
    
    .forgot-link {
      font-size: 0.875rem;
      color: $primary;
      font-weight: 500;
      text-decoration: none;
      &:hover { color: darken($primary, 10%); }
    }
  }

  // 登录按钮
  .login-btn {
    width: 100%;
    height: 52px; // 稍微高一点
    background-color: $primary;
    border-color: $primary;
    font-size: 1rem;
    font-weight: 600;
    letter-spacing: 0.025em;
    border-radius: 0.375rem;
    
    &:hover {
      background-color: darken($primary, 5%);
      transform: translateY(-1px); // 微动效
    }
  }

  // 底部Footer
  .form-footer {
      margin-top: 3rem;       // 距离上方按钮的间距
      width: 100%;            // 占满容器宽度
      display: flex;          // 使用 Flex 布局
      flex-direction: column; // 垂直排列
      align-items: center;    // 水平居中
      justify-content: center;
      
      .footer-lock {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        color: #94a3b8;       // Slate 400
        margin-bottom: 0.5rem;
        
        i {
          font-size: 1rem;
        }

        span {
          font-size: 0.75rem; // xs
          font-weight: 600;
          letter-spacing: 0.05em;
          text-transform: uppercase;
        }
      }
      
      .footer-note {
        font-size: 0.625rem;  // 10px
        color: #cbd5e1;       // Slate 300
        text-align: center;
      }
    }
}
</style>