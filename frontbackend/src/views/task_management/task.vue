<template>
  <div class="app-container">
    <div class="filter-container" :model="search_temp">
      <el-input v-model="search_temp.detect_name" placeholder="detect_name" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        Search
      </el-button>
      <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleCreate">
        Add
      </el-button>
    </div>

    <el-dialog :title="textMap[dialogDeleteStatus]" :visible.sync="dialogDeleteFormVisible">
      <el-table
        ref="viewtable"
        :key="tableKey"
        v-loading="deleteLoading"
        :data="deletedata"
        border
        fit
        highlight-current-row
        style="width: 100%;"
        @sort-change="sortChange"
      >
        <el-table-column label="ID" sortable="custom" align="center" width="80">
          <template slot-scope="scope">
            <span>{{ scope.row.id }}</span>
          </template>
        </el-table-column>

        <el-table-column label="detect_name" width="350px" align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.detect_name }}</span>
          </template>
        </el-table-column>
        <el-table-column label="detect_frency" width="350px" align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.detect_frency }}</span>
          </template>
        </el-table-column>
        <el-table-column label="detect_frency_unit" width="350px" align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.detect_frency_unit }}</span>
          </template>
        </el-table-column>
        <el-table-column label="effective_time" width="350px" align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.effective_time }}</span>
          </template>
        </el-table-column>
        <el-table-column label="effective_time_unit" width="350px" align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.effective_time_unit }}</span>
          </template>
        </el-table-column>
        <el-table-column label="Actions" align="center" width="300px" class-name="small-padding fixed-width">
          <template slot-scope="{row}">
            <el-button type="primary" size="mini" @click="deleteData(row)">
              Confirm
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>

    <el-table
      :key="tableKey"
      v-loading="listLoading"
      :data="list"
      border
      fit
      highlight-current-row
      style="width: 100%;"
      @sort-change="sortChange"
    >
      <el-table-column label="ID" sortable="custom" align="center" width="80">
        <template slot-scope="scope">
          <span>{{ scope.row.id }}</span>
        </template>
      </el-table-column>

      <el-table-column label="detect_name" width="350px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.detect_name }}</span>
        </template>
      </el-table-column>
      <el-table-column label="detect_frency" width="350px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.detect_frency }}</span>
        </template>
      </el-table-column>
      <el-table-column label="detect_frency_unit" width="350px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.detect_frency_unit }}</span>
        </template>
      </el-table-column>
      <el-table-column label="effective_time" width="350px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.effective_time }}</span>
        </template>
      </el-table-column>
      <el-table-column label="effective_time_unit" width="350px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.effective_time_unit }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Actions" align="center" width="400px" class-name="small-padding fixed-width">
        <template slot-scope="{row}">
          <el-button type="primary" size="mini" @click="handleUpdate(row)">
            Edit
          </el-button>
          <el-button v-if="row.status!='deleted'" size="mini" type="danger" @click="handleDelete(row)">
            Delete
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="page" :limit.sync="limit" @pagination="getList" />

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible">
      <el-form ref="dataForm" :model="temp" label-position="left" label-width="120px" style="width: 400px; margin-left:50px;">
        <el-form-item label="detect_name" prop="record">
          <el-input v-model="temp.detect_name" />
        </el-form-item>
        <el-form-item label="detect_frency" prop="record">
          <el-input v-model="temp.detect_frency" />
        </el-form-item>
        <el-form-item label="detect_frency_unit" prop="record">
          <el-select v-model="temp.detect_frency_unit" class="filter-item" placeholder="Please select">
            <el-option v-for="item in status_swicth" :key="item" :label="item" :value="item" />
          </el-select>
        </el-form-item>
        <el-form-item label="effective_time" prop="record">
          <el-input v-model="temp.effective_time" />
        </el-form-item>
        <el-form-item label="effective_time_unit" prop="record">
          <el-select v-model="temp.effective_time_unit" class="filter-item" placeholder="Please select">
            <el-option v-for="item in status_swicth" :key="item" :label="item" :value="item" />
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">
          Cancel
        </el-button>
        <el-button type="primary" @click="dialogStatus==='create'?createData():updateData()">
          Confirm
        </el-button>
      </div>
    </el-dialog>

    <el-dialog :visible.sync="dialogPvVisible" title="Reading statistics">
      <el-table :data="pvData" border fit highlight-current-row style="width: 100%">
        <el-table-column prop="key" label="Channel" />
        <el-table-column prop="pv" label="Pv" />
      </el-table>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="dialogPvVisible = false">Confirm</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { deleteid, fetchList, create, update } from '@/api/task'
import waves from '@/directive/waves' // waves directive
import { validateIP } from '@/utils/validate'
import Pagination from '@/components/Pagination' // secondary package based on el-pagination

const status_swicth = ['second', 'minute', 'hour', 'day', 'week', 'month']
export default {
  name: 'ComplexTable',
  components: { Pagination },
  directives: { waves },
  // filters: {
  //  statusFilter(status) {
  //    const statusMap = {
  //      published: 'success',
  //      draft: 'info',
  //      deleted: 'danger'
  //    }
  //    return statusMap[status]
  //  }
  // },
  data() {
    return {
      tableKey: 0,
      list: null,
      deletedata: null,
      total: 0,
      listLoading: true,
      deleteLoading: false,
      search_temp: {
        detect_name: ''
      },
      page: 1,
      limit: 10,
      status_swicth,
      temp: {
        detect_name: '',
        detect_frency: '',
        detect_frency_unit: '',
        effective_time: '',
        effective_time_unit: ''
      },
      dialogFormVisible: false,
      dialogDeleteFormVisible: false,
      dialogStatus: '',
      dialogDeleteStatus: '',
      textMap: {
        update: 'Edit',
        create: 'Create',
        delete: 'Delete'
      },
      dialogPvVisible: false,
      pvData: [],
      rules: {
        vip: [{ required: true, message: 'record is required', trigger: 'blur' }, { validator: validateIP, trigger: 'blur' }],
        record: [{ required: true, message: 'record is required', trigger: 'blur' }]
      }
    }
  },
  created() {
    this.getList()
  },
  methods: {
    getList() {
      this.listLoading = true
      fetchList({ 'taskname': this.search_temp.detect_name, 'page': this.page, 'size': this.limit }).then(response => {
        this.list = response.msg.results
        this.total = response.msg.count
        // Just to simulate the time of the request
        setTimeout(() => {
          this.listLoading = false
        }, 1.5 * 1000)
      })
    },
    handleFilter() {
      this.page = 1
      this.getList()
    },
    sortChange(data) {
      const { prop, order } = data
      if (prop === 'id') {
        this.sortByID(order)
      }
    },
    resetTemp() {
      this.temp = {
        node_isp: '',
        total_value: '',
        absolute_value: '',
        relative_rate: ''
      }
    },
    handleCreate() {
      this.resetTemp()
      this.dialogStatus = 'create'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    createData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          create(this.temp).then(() => {
            this.list.push(this.temp)
            this.dialogFormVisible = false
            this.$notify({
              title: 'Success',
              message: 'Created Successfully',
              type: 'success',
              duration: 2000
            })
          })
        }
      })
    },
    handleUpdate(row) {
      this.temp = Object.assign({}, row) // copy obj
      this.dialogStatus = 'update'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    updateData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.temp)
          var id = tempData.id
          delete tempData.id
          update(tempData, id).then(() => {
            for (const v of this.list) {
              if (v.id === this.temp.id) {
                const index = this.list.indexOf(v)
                this.list.splice(index, 1, this.temp)
                break
              }
            }
            this.dialogFormVisible = false
            this.$notify({
              title: 'Success',
              message: 'Update Successfully',
              type: 'success',
              duration: 2000
            })
          })
        }
      })
    },
    handleDelete(row) {
      var arr = []
      var tmp = {}
      for (var i in row) {
        tmp[i] = row[i]
      }
      arr.push(tmp)
      this.dialogDeleteStatus = 'delete'
      this.deleteLoading = true
      this.deletedata = arr
      this.dialogDeleteFormVisible = true
      setTimeout(() => {
        this.deleteLoading = false
      }, 1.5 * 1000)
    },
    deleteData(row) {
      var id = row.id
      deleteid(id).then(() => {
        for (var v of this.list) {
          if (v.id === row.id) {
            const index = this.list.indexOf(v)
            this.list.splice(index, 1)
            break
          }
        }
        this.dialogDeleteFormVisible = false
        this.$notify({
          title: 'Success',
          message: 'delete Successfully',
          type: 'success',
          duration: 2000
        })
      })
    }
  }
}
</script>
