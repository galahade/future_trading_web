<script setup>
import axios from "axios"
import { onBeforeMount, ref } from 'vue'
import { inject } from 'vue'
const config = {
    responseType: 'json',
};
const backend_host = inject('backend_host')
const tams_url = `${backend_host}/api/bottom/current_tips`
const now = ref(new Intl.DateTimeFormat("fr-CA", { year: "numeric", month: "2-digit", day: "2-digit" }).format(Date.now()))
const tableData = ref([])
const getDirection = (row) => {
    let direction = '买';
    let color = 'red';
    if (row.custom_symbol == 'S') {
        direction = '卖';
        color = 'green';
    }
    return { name: direction, color: color }
}
const getSymbolColor = (row) => {
    let color = 'green';
    if (row.count == 1) {
        color = 'red';
    }
    return color
}
const getPercentage = (row, column, cellValue, index) => {
    return cellValue * 100 + '%'

}
onBeforeMount(async () => {
    await axios.get(tams_url, config).then(res => {
        console.log(typeof res.data.data)
        tableData.value = res.data.data
    })
})
</script>

<template>
    <el-row>
        <el-col :span="24">
            <div class="grid-content ep-bg-purple-dark">摸底开仓提示:{{ now }}</div>
        </el-col>
    </el-row>
    <el-row>
        <el-col>
            <el-table :data="tableData" stripe style="width: 100%;" height="1000">
                <el-table-column fixed prop="datetime" label="时间" width="120" />
                <el-table-column fixed prop="symbol" label="合约" width="150">
                    <template #default="scope">
                        <span :style="{ color: getSymbolColor(scope.row) }">{{ scope.row.symbol }}</span>
                    </template>
                </el-table-column>
                <el-table-column prop="custom_symbol" label="方向" width="100">
                    <template #default="scope">
                        <span :style="{ color: getDirection(scope.row).color }">{{ getDirection(scope.row).name }}</span>
                    </template>
                </el-table-column>
                <el-table-column prop="count" label="七日内提示次数" width="150" />
                <el-table-column prop="pos" label="手数" width="150" />
                <el-table-column prop="last_price" label="最近收盘价" width="150" />
                <el-table-column prop="contract_m" label="合约乘数" width="150" />
                <el-table-column prop="open_pos_scale" label="开仓比例" :formatter="getPercentage" width="150" />
                <el-table-column prop="balance" label="资金总额" width="150" />
            </el-table>
        </el-col>
    </el-row>
</template>
<style lang="scss">
.el-row {
    margin-bottom: 20px;
}

.el-row:last-child {
    margin-bottom: 0;
}

.el-col {
    border-radius: 4px;
}

.grid-content {
    border-radius: 4px;
    min-height: 36px;
}
</style>