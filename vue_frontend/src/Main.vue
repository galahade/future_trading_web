<script lang="ts" setup>
import { ref } from 'vue'
import { Menu as IconMenu, Message, Setting } from '@element-plus/icons-vue'
import { RouterLink, RouterView } from 'vue-router'
import 'bootstrap/dist/css/bootstrap.min.css'
import { inject } from 'vue'

const backend_host = inject('backend_host')
console.log(backend_host)
const item = {
  date: '2016-05-02',
  name: 'Tom',
  address: 'No. 189, Grove St, Los Angeles',
}
const tableData = ref(Array.from({ length: 20 }).fill(item))
</script>
<template>
  <div class="wrapper">
    <!-- <el-container class="layout-container-demo" style="height: 1000px"> -->
    <el-container class="layout-container-demo fullheight">
      <el-aside width="200px">
        <el-scrollbar>
          <el-menu :default-openeds="['1']" :router="true">
            <el-sub-menu index="1">
              <template #title>
                <el-icon>
                  <message />
                </el-icon>摸底策略
              </template>
              <el-menu-item-group>
                <template #title>开仓提示</template>
                <el-menu-item index="1-1" route="/bottom/tams">当日开仓提示</el-menu-item>
                <el-menu-item index="1-2" route="/bottom/tams_history">全部开仓提示</el-menu-item>
              </el-menu-item-group>
              <el-menu-item-group title="配置">
                <el-menu-item index="1-3" route="/bottom/config">交易品种配置</el-menu-item>
              </el-menu-item-group>
              <el-sub-menu index="1-4">
                <template #title>Option4</template>
                <el-menu-item index="1-4-1">Option 4-1</el-menu-item>
              </el-sub-menu>
            </el-sub-menu>
            <el-sub-menu index="2">
              <template #title>
                <el-icon><icon-menu /></el-icon>主策略
              </template>
              <el-menu-item-group>
                <template #title>交易信息</template>
                <el-menu-item index="2-1" route="/main/trading">当前开仓情况</el-menu-item>
                <el-menu-item index="2-2" route="/main/alltradeposinfo">全部开平仓情况</el-menu-item>
                <el-menu-item index="2-2" route="/main/allclosedposinfo">全部平仓情况</el-menu-item>
              </el-menu-item-group>
            </el-sub-menu>
          </el-menu>
        </el-scrollbar>
      </el-aside>
      <el-container>
        <el-header style="text-align: right; font-size: 12px">
          <div class="toolbar">
            <el-dropdown>
              <el-icon style="margin-right: 8px; margin-top: 1px">
                <setting />
              </el-icon>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item>View</el-dropdown-item>
                  <el-dropdown-item>Add</el-dropdown-item>
                  <el-dropdown-item>Delete</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
            <span>Tom</span>
          </div>
        </el-header>
        <el-main>
          <el-scrollbar>
            <RouterView />
          </el-scrollbar>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<style scoped>
.wrapper {
  display: flex;
  place-items: flex-start;
  flex-wrap: wrap;
  width: 1500px;
  text-align: left;
}

@media (min-width: 1024px) {
  .layout-container-demo .el-header {
    position: relative;
    background-color: var(--el-color-primary-light-7);
    color: var(--el-text-color-primary);
  }

  .layout-container-demo .el-aside {
    color: var(--el-text-color-primary);
    background: var(--el-color-primary-light-8);
  }

  .layout-container-demo .el-menu {
    border-right: none;
  }

  .layout-container-demo .el-main {
    padding: 0;
  }

  .layout-container-demo .toolbar {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    right: 20px;
  }
}
</style>