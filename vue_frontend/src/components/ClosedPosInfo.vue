<script setup>
import axios from "axios"
import { onBeforeMount, ref, inject } from 'vue'
import Numeral from "numeral"

const backend_host = inject('backend_host')
const tams_url = `${backend_host}/api/main/allclosedposinfo`
const now = ref(new Intl.DateTimeFormat("fr-CA", { year: "numeric", month: "2-digit", day: "2-digit" }).format(Date.now()))
const tableData = ref([])
const getDirection = (row) => {
    let direction = '买';
    let color = 'green';
    if (row.custom_symbol == 'S') {
        direction = '卖';
        color = 'red';
    }
    return { name: direction, color: color }
}

const getPercentage = (row, column, cellValue, index) => {
    return cellValue * 100 + '%'
}

const priceFormatter = (row, column, cellValue, index) => {
    return Numeral(cellValue).format('0.00')
}

onBeforeMount(async () => {
    await axios.get(tams_url).then((res) => {
        console.log(typeof res.data);
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
            <el-table :data="tableData" row-key="id" border default-expand-all :tree-props="{ children: 'closePosInfos' }"
                stripe style="width: 100%;" height="1000">
                <el-table-column fixed sortable prop="symbol" label="合约" width="160">
                </el-table-column>
                <el-table-column sortable prop="custom_symbol" align="center" label="方向" width="80">
                    <template #default="scope">
                        <span :style="{ color: getDirection(scope.row).color }">{{ getDirection(scope.row).name }}</span>
                    </template>
                </el-table-column>
                <el-table-column sortable prop="datetime" align="center" label="开/平仓时间" width="110" />
                <el-table-column prop="pos" align="right" label="开/平仓手数" width="90" />
                <el-table-column prop="price" align="right" label="开/平仓价格" :formatter="priceFormatter" width="100" />
                <el-table-column prop="slp" align="right" label="止损价" :formatter="priceFormatter" width="100" />
                <el-table-column prop="spp" align="right" label="止盈起始价" :formatter="priceFormatter" width="100" />
                <el-table-column prop="commission" align="right" label="手续费" :formatter="priceFormatter" width="100" />
                <el-table-column sortable prop="daily_cond" align="center" label="日线条件" width="110" />
                <el-table-column sortable prop="h3_cond" align="center" label="3小时条件" width="110" />
                <el-table-column sortable prop="close_reason" align="center" label="平仓原因" width="150" />
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