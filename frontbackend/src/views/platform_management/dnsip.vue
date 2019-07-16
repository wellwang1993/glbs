<template>
  <div class="app-container">
    <div class="filter-container" :model="search_temp">
      <el-input v-model="search_temp.dns_ip" placeholder="dnsip" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        Search
      </el-button>
      <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleCreate">
        Add
      </el-button>
    </div>

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
      <el-table-column label="ID" prop="id" sortable="custom" align="center" width="80">
        <template slot-scope="scope">
          <span>{{ scope.row.id }}</span>
        </template>
      </el-table-column>

      <el-table-column label="dnsip" width="350px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.dns_ip }}</span>
        </template>
      </el-table-column>

      <el-table-column label="dnsstatus" width="350px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.dns_status }}</span>
        </template>
      </el-table-column>
      <el-table-column label="dnsscribe" width="350px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.dns_describe }}</span>
        </template>
      </el-table-column>
      <el-table-column label="dns_name" width="350px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.dns_type.dns_name }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Actions" align="center" width="300px" class-name="small-padding fixed-width">
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
        <el-table-column label="ID" prop="id" sortable="custom" align="center" width="80">
          <template slot-scope="scope">
            <span>{{ scope.row.id }}</span>
          </template>
        </el-table-column>

        <el-table-column label="dnsip" width="350px" align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.dns_ip }}</span>
          </template>
        </el-table-column>

        <el-table-column label="dnsstatus" width="350px" align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.dns_status }}</span>
          </template>
        </el-table-column>
        <el-table-column label="dnsscribe" width="350px" align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.dns_describe }}</span>
          </template>
        </el-table-column>
        <el-table-column label="dns_name" width="350px" align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.dns_type.dns_name }}</span>
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

    <pagination v-show="total>0" :total="total" :page.sync="page" :limit.sync="limit" @pagination="getList" />

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible">
      <el-form ref="dataForm" :model="temp" label-position="left" label-width="70px" style="width: 400px; margin-left:50px;">
        <el-form-item label="Dnsip" prop="record">
          <el-input v-model="temp.dns_ip" />
        </el-form-item>
        <el-form-item label="Status" prop="record">
          <el-select v-model="temp.dns_status" class="filter-item" placeholder="Please select">
            <el-option v-for="item in status_swicth" :key="item" :label="item" :value="item" />
          </el-select>
        </el-form-item>
        <el-form-item label="Describe">
          <el-input v-model="temp.dns_describe" :autosize="{ minRows: 2, maxRows: 4}" type="textarea" placeholder="Please input" />
        </el-form-item>
        <el-form-item label="Dnstype" prop="record">
          <el-select v-model="temp.dns_type" class="filter-item" placeholder="Please select">
            <el-option v-for="item in dnstypelist" :key="item.dns_name" :label="item.dns_name" :value="item.id" />
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
import { fetchDnstype, deleteid, fetchList, create, update } from '@/api/dnsip'
import waves from '@/directive/waves' // waves directive
import Pagination from '@/components/Pagination' // secondary package based on el-pagination

const status_swicth = ['enable', 'disable']
// arr to obj, such as { CN : "China", US : "USA" }

export default {
  name: 'ComplexTable',
  components: { Pagination },
  directives: { waves },
  data() {
    return {
      tableKey: 0,
      list: null,
      deletedata: null,
      dnstypelist: '',
      total: 0,
      listLoading: true,
      deleteLoading: false,
      search_temp: {
        dns_name: ''
      },
      page: 1,
      limit: 10,
      status_swicth,
      temp: {
        dns_ip: '',
        dns_status: '',
        dns_type: '',
        dns_describe: ''
      },
      dialogFormVisible: false,
      dialogDeleteFormVisible: false,
      dialogStatus: '',
      dialogDeleteStatus: '',
      textMap: {
        update: 'Edit',
        delete: 'Delete',
        create: 'Create'
      },
      dialogPvVisible: false,
      pvData: [],
      rules: {
        record: [{ required: true, message: 'record is required', trigger: 'blur' }]
      }
    }
  },
  created() {
    this.getList()
    this.getDnstype()
  },
  methods: {
    getList() {
      this.listLoading = true
      fetchList({ 'dnsip': this.search_temp.dns_name, 'page': this.page, 'size': this.limit }).then(response => {
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
        dns_ip: '',
        dns_status: '',
        dns_type: '',
        dns_describe: ''
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
      var dnsname = this.temp.dns_type.id
      delete this.temp.dns_type
      this.$set(this.temp, 'dns_type', dnsname)
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
    },
    getDnstype() {
      fetchDnstype().then(response => {
        this.dnstypelist = response.msg
      })
    }
  }
}
</script>
