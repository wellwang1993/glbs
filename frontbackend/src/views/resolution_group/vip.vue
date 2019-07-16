<template>
  <div class="app-container">
    <div class="filter-container" :model="search_temp">
      <el-input v-model="search_temp.nodeid" placeholder="nodeid" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-input v-model="search_temp.ip" placeholder="address" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        Search
      </el-button>
      <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleCreate">
        Add
      </el-button>
      <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleUpDown">
        Vipupdown
      </el-button>
      <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleApplicability">
        Vipapplicability
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
      <el-table-column label="ID" sortable="custom" align="center" width="80">
        <template slot-scope="scope">
          <span>{{ scope.row.id }}</span>
        </template>
      </el-table-column>

      <el-table-column label="node_id" width="350px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.node_id }}</span>
        </template>
      </el-table-column>
      <el-table-column label="address" width="350px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.vip_address }}</span>
        </template>
      </el-table-column>
      <el-table-column label="vip_status" width="350px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.vip_status }}</span>
        </template>
      </el-table-column>

      <el-table-column label="vip_bandwidth" width="350px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.vip_bandwidth }}</span>
        </template>
      </el-table-column>
      <el-table-column label="vip_enable_switch" width="350px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.vip_enable_switch }}</span>
        </template>
      </el-table-column>
      <el-table-column label="node_country" width="350px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.node_country }}</span>
        </template>
      </el-table-column>
      <el-table-column label="node_isp" width="350px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.node_isp }}</span>
        </template>
      </el-table-column>
      <el-table-column label="node_region" width="350px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.node_region }}</span>
        </template>
      </el-table-column>
      <el-table-column label="node_province" width="350px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.node_province }}</span>
        </template>
      </el-table-column>
      <el-table-column label="node_city" width="350px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.node_city }}</span>
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
        <el-table-column label="node_id" width="350px" align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.node_id }}</span>
          </template>
        </el-table-column>
        <el-table-column label="address" width="350px" align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.vip_address }}</span>
          </template>
        </el-table-column>
        <el-table-column label="vip_status" width="350px" align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.vip_status }}</span>
          </template>
        </el-table-column>
        <el-table-column label="vip_bandwidth" width="350px" align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.vip_bandwidth }}</span>
          </template>
        </el-table-column>
        <el-table-column label="vip_enable_switch" width="350px" align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.vip_enable_switch }}</span>
          </template>
        </el-table-column>
        <el-table-column label="node_country" width="350px" align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.node_country }}</span>
          </template>
        </el-table-column>
        <el-table-column label="node_isp" width="350px" align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.node_isp }}</span>
          </template>
        </el-table-column>
        <el-table-column label="node_region" width="350px" align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.node_region }}</span>
          </template>
        </el-table-column>
        <el-table-column label="node_province" width="350px" align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.node_province }}</span>
          </template>
        </el-table-column>
        <el-table-column label="node_city" width="350px" align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.node_city }}</span>
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

    <el-dialog :title="textMap[dialogApplicabilityStatus]" :visible.sync="dialogFormApplicabilityVisible">
      <el-form ref="dataApplicabilityForm" :model="status_temp" label-position="left" label-width="120px" style="width: 400px; margin-left:50px;">
        <el-form-item label="vip_status" prop="record">
          <el-select v-model="status_temp.vip_status" class="filter-item" placeholder="Please select">
            <el-option v-for="item in status_swicth" :key="item" :label="item" :value="item" />
          </el-select>
        </el-form-item>
        <el-form-item label="vip_enable_switch" prop="record">
          <el-select v-model="status_temp.vip_enable_switch" class="filter-item" placeholder="Please select">
            <el-option v-for="item in status_swicth" :key="item" :label="item" :value="item" />
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormApplicabilityVisible = false">
          Cancel
        </el-button>
        <el-button type="primary" @click="updateApplicability()">
          Confirm
        </el-button>
      </div>
    </el-dialog>
    <el-dialog :title="textMap[dialogUpdownStatus]" :visible.sync="dialogFormUpdownVisible">
      <el-form ref="dataUpdownForm" :model="updown_temp" label-position="left" label-width="120px" style="width: 400px; margin-left:50px;">
        <el-form-item label="vip_status" prop="record">
          <el-select v-model="updown_temp.vip_status" class="filter-item" placeholder="Please select">
            <el-option v-for="item in status_swicth" :key="item" :label="item" :value="item" />
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormUpdownVisible = false">
          Cancel
        </el-button>
        <el-button type="primary" @click="vipUpDown()">
          Confirm
        </el-button>
      </div>
    </el-dialog>
    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible">
      <el-form ref="dataForm" :model="temp" label-position="left" label-width="120px" style="width: 400px; margin-left:50px;">
        <el-form-item label="node_id" prop="record">
          <el-input v-model="temp.node_id" />
        </el-form-item>
        <el-form-item label="vip_status" prop="record">
          <el-select v-model="temp.vip_status" class="filter-item" placeholder="Please select">
            <el-option v-for="item in status_swicth" :key="item" :label="item" :value="item" />
          </el-select>
        </el-form-item>
        <el-form-item label="vip_enable_switch" prop="record">
          <el-select v-model="temp.vip_enable_switch" class="filter-item" placeholder="Please select">
            <el-option v-for="item in status_swicth" :key="item" :label="item" :value="item" />
          </el-select>
        </el-form-item>
        <el-form-item label="vip_address" prop="vip">
          <el-input v-model="temp.vip_address" />
        </el-form-item>
        <el-form-item label="vip_bandwidth" prop="record">
          <el-input v-model="temp.vip_bandwidth" />
        </el-form-item>
        <el-form-item label="node_country" prop="record">
          <el-input v-model="temp.node_country" />
        </el-form-item>
        <el-form-item label="node_isp" prop="record">
          <el-input v-model="temp.node_isp" />
        </el-form-item>
        <el-form-item label="node_region" prop="record">
          <el-input v-model="temp.node_region" />
        </el-form-item>
        <el-form-item label="node_province" prop="record">
          <el-input v-model="temp.node_province" />
        </el-form-item>
        <el-form-item label="node_city" prop="record">
          <el-input v-model="temp.node_city" />
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
import { vipApplicability, vipUpdown, deleteid, fetchList, create, update } from '@/api/vip'
import waves from '@/directive/waves' // waves directive
import { validateIP } from '@/utils/validate'
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
      total: 0,
      listLoading: true,
      deleteLoading: true,
      search_temp: {
        nodeid: '',
        ip: ''
      },
      page: 1,
      limit: 10,
      status_swicth,
      temp: {
        node_id: '',
        vip_status: '',
        vip_address: '',
        vip_bandwidth: '',
        vip_enable_switch: '',
        node_country: '',
        node_isp: '',
        node_region: '',
        node_province: '',
        node_city: ''
      },
      status_temp: {
        vip_status: '',
        vip_enable_switch: ''
      },
      updown_temp: {
        vip_status: ''
      },
      dialogFormVisible: false,
      dialogDeleteFormVisible: false,
      dialogFormApplicabilityVisible: false,
      dialogFormUpdownVisible: false,
      dialogStatus: '',
      dialogDeleteStatus: '',
      dialogApplicabilityStatus: '',
      dialogUpdownStatus: '',
      textMap: {
        update: 'Edit',
        create: 'Create',
        delete: 'Delete',
        applicabilitystatus: 'Applicabilitystatus',
        updownstatus: 'UpDownstatus'
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
      // fetchList(currentPage).then(response => {
      fetchList({ 'nodeid': this.search_temp.nodeid, 'ip': this.search_temp.ip, 'page': this.page, 'size': this.limit }).then(response => {
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
        node_id: '',
        vip_status: '',
        vip_address: '',
        vip_bandwidth: '',
        vip_enable_switch: '',
        node_country: '',
        node_isp: '',
        node_region: '',
        node_province: '',
        node_city: ''
      }
    },
    handleApplicability() {
      this.dialogApplicabilityStatus = 'applicabilitystatus'
      this.dialogFormApplicabilityVisible = true
      this.$nextTick(() => {
        this.$refs['dataApplicabilityForm'].clearValidate()
      })
    },
    updateApplicability() {
      vipApplicability({ 'noderesource': this.search_temp.nodeid, 'ipresource': this.search_temp.ip, 'artificialstatus': this.status_temp.vip_status, 'detectstatus': this.status_temp.vip_enable_switch }).then(() => {
        this.dialogFormApplicabilityVisible = false
        this.$notify({
          title: 'Success',
          message: 'Created Successfully',
          type: 'success',
          duration: 2000
        })
      })
      this.status_temp = {
        vip_status: '',
        vip_enable_switch: ''
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
    },
    handleUpDown() {
      this.dialogUpdownStatus = 'updownstatus'
      this.dialogFormUpdownVisible = true
      this.$nextTick(() => {
        this.$refs['dataUpdownForm'].clearValidate()
      })
    },
    vipUpDown() {
      vipUpdown({ 'status': this.updown_temp.vip_status, 'noderesource': this.search_temp.nodeid, 'ipresource': this.search_temp.ip }).then(() => {
        this.dialogFormUpdownVisible = false
        this.$notify({
          title: 'Success',
          message: 'Created Successfully',
          type: 'success',
          duration: 2000
        })
        this.updown_temp = {
          vip_status: ''
        }
      })
    }
  }
}
</script>
