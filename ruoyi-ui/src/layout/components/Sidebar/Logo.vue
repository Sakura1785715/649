<template>
  <div class="sidebar-logo-container" :class="{'collapse':collapse}" :style="{ backgroundColor: sideTheme === 'theme-dark' ? variables.menuBackground : variables.menuLightBackground }">
    <transition name="sidebarLogoFade">
      <router-link v-if="collapse" key="collapse" class="sidebar-logo-link" to="/">
        <svg class="sidebar-train-logo" viewBox="0 0 24 24" fill="none" :stroke="sideTheme === 'theme-dark' ? '#FFFFFF' : '#2563EB'" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.2">
          <path d="M21 21H3V11.2C3 6.671 6.671 3 11.2 3H12.8C17.329 3 21 6.671 21 11.2V21Z"></path>
          <path d="M3 15H21"></path><path d="M9 21V23"></path><path d="M15 21V23"></path>
          <path d="M3 11H21"></path><circle cx="7" cy="18" r="1.5"></circle>
          <circle cx="17" cy="18" r="1.5"></circle><path d="M8 7H16"></path>
        </svg>
      </router-link>
      
      <router-link v-else key="expand" class="sidebar-logo-link" to="/">
        <svg class="sidebar-train-logo" viewBox="0 0 24 24" fill="none" :stroke="sideTheme === 'theme-dark' ? '#FFFFFF' : '#2563EB'" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.2">
          <path d="M21 21H3V11.2C3 6.671 6.671 3 11.2 3H12.8C17.329 3 21 6.671 21 11.2V21Z"></path>
          <path d="M3 15H21"></path><path d="M9 21V23"></path><path d="M15 21V23"></path>
          <path d="M3 11H21"></path><circle cx="7" cy="18" r="1.5"></circle>
          <circle cx="17" cy="18" r="1.5"></circle><path d="M8 7H16"></path>
        </svg>
        <h1 class="sidebar-title" :style="{ color: sideTheme === 'theme-dark' ? variables.logoTitleColor : variables.logoLightTitleColor }">{{ title }}</h1>
      </router-link>
    </transition>
  </div>
</template>

<script>
import variables from '@/assets/styles/variables.scss'

export default {
  name: 'SidebarLogo',
  props: {
    collapse: {
      type: Boolean,
      required: true
    }
  },
  computed: {
    variables() {
      return variables;
    },
    sideTheme() {
      return this.$store.state.settings.sideTheme
    }
  },
  data() {
    return {
      title: 'CRH-PHM System' // 这里修改为你系统侧边栏的名字
    }
  }
}
</script>

<style lang="scss" scoped>
.sidebarLogoFade-enter-active {
  transition: opacity 1.5s;
}

.sidebarLogoFade-enter,
.sidebarLogoFade-leave-to {
  opacity: 0;
}

.sidebar-logo-container {
  position: relative;
  width: 100%;
  height: 50px;
  line-height: 50px;
  background: #2b2f3a;
  text-align: center;
  overflow: hidden;

  & .sidebar-logo-link {
    height: 100%;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;

    // 重点：小火车 SVG 的专属样式
    & .sidebar-train-logo {
      width: 28px;
      height: 28px;
      margin-right: 12px;
      transition: all 0.3s;
    }

    & .sidebar-title {
      margin: 0;
      color: #fff;
      font-weight: 600;
      line-height: 50px;
      font-size: 14px;
      font-family: Avenir, Helvetica Neue, Arial, Helvetica, sans-serif;
      vertical-align: middle;
      letter-spacing: 0.05em;
    }
  }

  &.collapse {
    .sidebar-logo-link {
      justify-content: center;
      .sidebar-train-logo {
        margin-right: 0px; // 折叠时去掉右边距，让图标居中
      }
    }
  }
}
</style>