<template>
  <div class="app-container">
    <div class="filter-container" :model="search_temp">
      <el-input v-model="search_temp.nodeid" placeholder="nodeid" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-input v-model="search_temp.adminip" placeholder="adminip" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-input v-model="search_temp.country" placeholder="country" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-input v-model="search_temp.isp" placeholder="isp" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-input v-model="search_temp.region" placeholder="region" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-input v-model="search_temp.province" placeholder="province" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-input v-model="search_temp.city" placeholder="city" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        Search
      </el-button>
      <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleCreate">
        Add
      </el-button>
      <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleQosSwitch">
        QosSwitch
      </el-button>
      <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleApplicabilitySwitch">
        ApplicabilitySwitch
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

        <el-table-column label="node_id" width="350px" align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.node_id }}</span>
          </template>
        </el-table-column>
        <el-table-column label="adminip" width="350px" align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.admin_ip }}</span>
          </template>
        </el-table-column>
        <el-table-column label="node_country" width="350px" align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.country }}</span>
          </template>
        </el-table-column>
        <el-table-column label="node_isp" width="350px" align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.isp }}</span>
          </template>
        </el-table-column>
        <el-table-column label="node_region" width="350px" align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.region }}</span>
          </template>
        </el-table-column>
        <el-table-column label="node_province" width="350px" align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.province }}</span>
          </template>
        </el-table-column>
        <el-table-column label="node_city" width="350px" align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.city }}</span>
          </template>
        </el-table-column>
        <el-table-column label="availability_status" width="350px" align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.availability_status }}</span>
          </template>
        </el-table-column>
        <el-table-column label="qos_status" width="350px" align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.qos_status }}</span>
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

      <el-table-column label="node_id" width="350px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.node_id }}</span>
        </template>
      </el-table-column>
      <el-table-column label="adminip" width="350px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.admin_ip }}</span>
        </template>
      </el-table-column>
      <el-table-column label="node_country" width="350px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.country }}</span>
        </template>
      </el-table-column>
      <el-table-column label="node_isp" width="350px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.isp }}</span>
        </template>
      </el-table-column>
      <el-table-column label="node_region" width="350px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.region }}</span>
        </template>
      </el-table-column>
      <el-table-column label="node_province" width="350px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.province }}</span>
        </template>
      </el-table-column>
      <el-table-column label="node_city" width="350px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.city }}</span>
        </template>
      </el-table-column>
      <el-table-column label="availability_status" width="350px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.availability_status }}</span>
        </template>
      </el-table-column>
      <el-table-column label="qos_status" width="350px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.qos_status }}</span>
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
          <el-button v-if="row.status!='deleted'" size="mini" type="danger" @click="handleIpAdd(row)">
            add
          </el-button>
          <el-button v-if="row.status!='deleted'" size="mini" type="danger" @click="handleIpCancel(row)">
            cancel
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="page" :limit.sync="limit" @pagination="getList" />

    <el-dialog :title="textMap[dialogQosStatus]" :visible.sync="dialogFormQosVisible">
      <el-form ref="dataQosForm" :model="qos_status" label-position="left" label-width="120px" style="width: 400px; margin-left:50px;">
        <el-form-item label="qosstatus" prop="record">
          <el-select v-model="qos_status" class="filter-item" placeholder="Please select">
            <el-option v-for="item in status_swicth" :key="item" :label="item" :value="item" />
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormQosVisible = false">
          Cancel
        </el-button>
        <el-button type="primary" @click="handleQos()">
          Confirm
        </el-button>
      </div>
    </el-dialog>
    <el-dialog :title="textMap[dialogApplicabilityStatus]" :visible.sync="dialogFormApplicabilityVisible">
      <el-form ref="dataApplicabilityForm" :model="availability_status" label-position="left" label-width="120px" style="width: 400px; margin-left:50px;">
        <el-form-item label="availability_status" prop="record">
          <el-select v-model="availability_status" class="filter-item" placeholder="Please select">
            <el-option v-for="item in status_swicth" :key="item" :label="item" :value="item" />
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormApplicabilityVisible = false">
          Cancel
        </el-button>
        <el-button type="primary" @click="handleApplicability()">
          Confirm
        </el-button>
      </div>
    </el-dialog>
    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible">
      <el-form ref="dataForm" :model="temp" label-position="left" label-width="120px" style="width: 400px; margin-left:50px;">
        <el-form-item label="node_id" prop="record">
          <el-input v-model="temp.node_id" />
        </el-form-item>
        <el-form-item label="admin_ip" prop="record">
          <el-input v-model="temp.admin_ip" />
        </el-form-item>
        <el-form-item label="availability_status" prop="record">
          <el-select v-model="temp.availability_status" class="filter-item" placeholder="Please select">
            <el-option v-for="item in status_swicth" :key="item" :label="item" :value="item" />
          </el-select>
        </el-form-item>
        <el-form-item label="qos_status" prop="record">
          <el-select v-model="temp.qos_status" class="filter-item" placeholder="Please select">
            <el-option v-for="item in status_swicth" :key="item" :label="item" :value="item" />
          </el-select>
        </el-form-item>
        <el-form-item label="node_country" prop="record">
          <el-input v-model="temp.country" />
        </el-form-item>
        <el-form-item label="node_isp" prop="record">
          <el-input v-model="temp.isp" />
        </el-form-item>
        <el-form-item label="node_region" prop="record">
          <el-input v-model="temp.region" />
        </el-form-item>
        <el-form-item label="node_province" prop="record">
          <el-input v-model="temp.province" />
        </el-form-item>
        <el-form-item label="node_city" prop="record">
          <el-input v-model="temp.city" />
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
import { deleteid, fetchList, create, update, updateApplicability, updateQos } from '@/api/probe'
import waves from '@/directive/waves' // waves directive
import { validateIP } from '@/utils/validate'
import Pagination from '@/components/Pagination' // secondary package based on el-pagination

const status_swicth = ['enable', 'disable']
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
        nodeid: '',
        adminip: '',
        country: '',
        isp: '',
        region: '',
        province: '',
        city: ''
      },
      page: 1,
      limit: 10,
      status_swicth,
      temp: {
        node_id: '',
        admin_ip: '',
        country: '',
        isp: '',
        region: '',
        province: '',
        city: '',
        availability_status: '',
        qos_status: ''
      },
      iplist_temp: [],
      qos_status: '',
      availability_status: '',
      dialogFormVisible: false,
      dialogDeleteFormVisible: false,
      dialogFormQosVisible: false,
      dialogFormApplicabilityVisible: false,
      dialogStatus: '',
      dialogDeleteStatus: '',
      dialogQosStatus: '',
      dialogApplicabilityStatus: '',
      textMap: {
        update: 'Edit',
        create: 'Create',
        delete: 'Delete',
        qosstatus: 'QosStatus',
        applicabilitystatus: 'ApplicabilityStatus'
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
      fetchList({ 'nodeid': this.search_temp.nodeid, 'adminip': this.search_temp.adminip, 'country': this.search_temp.country, 'isp': this.search_temp.isp, 'region': this.search_temp.region, 'province': this.search_temp.province, 'city': this.search_temp.city, 'page': this.page, 'size': this.limit }).then(response => {
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
        admin_ip: '',
        country: '',
        isp: '',
        region: '',
        province: '',
        city: '',
        availability_status: '',
        qos_status: ''
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
    handleIpAdd(row) {
      this.iplist_temp.push(row.id)
      this.$notify({
        title: 'Success',
        message: 'Add Successfully',
        type: 'success',
        duration: 2000
      })
    },
    handleIpCancel(row) {
      var index = this.iplist_temp.indexOf(row.id)
      if (index !== -1) {
        this.iplist_temp.splice(index, 1)
      }
      this.$notify({
        title: 'Success',
        message: 'Cancel Successfully',
        type: 'success',
        duration: 2000
      })
    },
    handleQosSwitch() {
      this.dialogQosStatus = 'qosstatus'
      this.dialogFormQosVisible = true
      this.$nextTick(() => {
        this.$refs['dataQosForm'].clearValidate()
      })
    },
    handleApplicabilitySwitch() {
      this.dialogApplicabilityStatus = 'applicabilitystatus'
      this.dialogFormApplicabilityVisible = true
      this.$nextTick(() => {
        this.$refs['dataApplicabilityForm'].clearValidate()
      })
    },
    handleQos() {
      updateQos({ 'status': this.qos_status, 'resourceinfo': this.iplist_temp, 'switchtype': 'qos' }).then(() => {
        this.dialogFormQosVisible = false
        this.$notify({
          title: 'Success',
          message: 'Created Successfully',
          type: 'success',
          duration: 2000
        })
      })
      this.qos_status = ''
      this.iplist_temp = []
    },
    handleApplicability() {
      updateApplicability({ 'status': this.availability_status, 'resourceinfo': this.iplist_temp, 'switchtype': 'availability' }).then(() => {
        this.dialogFormApplicabilityVisible = false
        this.$notify({
          title: 'Success',
          message: 'Created Successfully',
          type: 'success',
          duration: 2000
        })
      })
      this.availability_status = ''
      this.iplist_temp = []
    }
  }
}
</script>
