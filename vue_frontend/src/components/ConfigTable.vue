<script setup>
import axios from "axios"
import { onBeforeMount, ref } from 'vue'
import 'bootstrap/dist/css/bootstrap.min.css'
import { InfoFilled } from '@element-plus/icons-vue'
import { inject } from 'vue'

const backend_host = inject('backend_host')
const config_change_url = `${backend_host}/api/bottom/`
const config_display_url = `${backend_host}/api/bottom/config`
console.log(config_display_url)
const now = ref(new Intl.DateTimeFormat("fr-CA", { year: "numeric", month: "2-digit", day: "2-digit" }).format(Date.now()))
const tableData = ref([]);
const tableRowClassName = ({ row, rowIndex }) => {
    if (row.is_active) {
        return 'success-row'
    } else {
        return ''
    }
}
const changeActiveStatus = (index, row) => {
    let url = config_change_url + row.id
    axios.post(url, {
        headers: {
            'Content-Type': 'application/json',
        },
        data: { "is_active": !row.is_active }
    }).then(res => {
        console.log(res.data)
        if (res.data.success) {
            row.is_active = !row.is_active
        }
    })
}
const cancelEvent = () => {
    console.log('cancel!')
}
const getPercentage = (row, column, cellValue, index) => {
    return cellValue * 100 + '%'

}
onBeforeMount(async () => {
    await axios.get(config_display_url).then(res => tableData.value = res.data.data)
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
            <el-table :data="tableData" stripe height="1000" :row-class-name="tableRowClassName">
                <el-table-column fixed prop="name" label="合约名" width="150" />
                <el-table-column fixed sortable prop="symbol" label="主联合约" width="150" />
                <el-table-column sortable prop="is_active" label="是否交易" width="150">
                    <template #default="scope">
                        <el-radio-group disabled v-model="scope.row.is_active" size="small">
                            <el-radio-button label=true>是</el-radio-button>
                            <el-radio-button label=false>否</el-radio-button>
                        </el-radio-group>
                    </template>
                </el-table-column>
                <el-table-column prop="contract_m" label="合约乘数" width="150" />
                <el-table-column prop="open_pos_scale" label="开仓比例" :formatter="getPercentage" width="150" />
                <el-table-column label="Operations">
                    <template #default="scope">
                        <el-popconfirm confirm-button-text="是" cancel-button-text="否" :icon="InfoFilled"
                            icon-color="#626AEF" title="确认修改交易状态吗?"
                            @confirm="$event => changeActiveStatus(scope.$index, scope.row)" @cancel="cancelEvent">
                            <template #reference>
                                <el-button size="small" type="danger">修改状态</el-button>
                            </template>
                        </el-popconfirm>
                    </template>
                </el-table-column>
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

.el-table .success-row {
    color: red;
    font-weight: bold;
}
</style>