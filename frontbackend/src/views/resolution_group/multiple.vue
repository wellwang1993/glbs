<template>
  <div class="app-container">
    <div class="filter-container" :model="search_temp">
      <el-input v-model="search_temp.zone_name" placeholder="zonename" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-select v-model="listQuery.sort" style="width: 140px" class="filter-item" @change="handleFilter">
        <el-option v-for="item in sortOptions" :key="item.key" :label="item.label" :value="item.key" />
      </el-select>
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        Search
      </el-button>
      <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleCreate">
        Add
      </el-button>
      <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleGenerate">
        Generate
      </el-button>
      <el-checkbox v-model="showReviewer" class="filter-item" style="margin-left:15px;" @change="tableKey=tableKey+1">
        reviewer
      </el-checkbox>
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

      <el-table-column label="zonename" width="350px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.zone_name.zone_name }}</span>
        </template>
      </el-table-column>
      <el-table-column label="record_name" width="350px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.record_name }}</span>
        </template>
      </el-table-column>

      <el-table-column label="record_content" width="350px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.record_content }}</span>
        </template>
      </el-table-column>
      <el-table-column label="record_type" width="350px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.record_type }}</span>
        </template>
      </el-table-column>
      <el-table-column label="internet_type" width="350px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.internet_type }}</span>
        </template>
      </el-table-column>
      <el-table-column label="record_ttl" width="350px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.record_ttl }}</span>
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

    <pagination v-show="total>0" :total="total" :page.sync="page" :limit.sync="listQuery.limit" @pagination="getList" />

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible">
      <el-form ref="dataForm" :model="temp" label-position="left" label-width="120px" style="width: 400px; margin-left:50px;">
        <el-form-item label="Zonename" prop="record">
          <el-select v-model="temp.zone_name" class="filter-item" placeholder="Please select">
            <el-option v-for="item in zonenamelist" :key="item.zone_name" :label="item.zone_name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="Recordname" prop="record">
          <el-input v-model="temp.record_name" />
        </el-form-item>
        <el-form-item label="Recordcontent" prop="record">
          <el-input v-model="temp.record_content" />
        </el-form-item>
        <el-form-item label="Recordtype" prop="record">
          <el-input v-model="temp.record_type" />
        </el-form-item>
        <el-form-item label="Internettype" prop="record">
          <el-input v-model="temp.internet_type" />
        </el-form-item>
        <el-form-item label="Recordttl" prop="record">
          <el-input v-model="temp.record_ttl" />
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
        <el-button type="primary" @click="dialogStatus==='create'?createData():modifyData()">
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
import { generateConfig, fetchDnstype, fetchZone, deleteid, fetchList, fetchOne, create, update } from '@/api/zone'
import waves from '@/directive/waves' // waves directive
import { parseTime } from '@/utils'
import Pagination from '@/components/Pagination' // secondary package based on el-pagination

const calendarTypeOptions = [
  { key: 'CN', display_name: 'China' },
  { key: 'US', display_name: 'USA' },
  { key: 'JP', display_name: 'Japan' },
  { key: 'EU', display_name: 'Eurozone' }
]
const status_swicth = ['enable', 'disable']
// arr to obj, such as { CN : "China", US : "USA" }
const calendarTypeKeyValue = calendarTypeOptions.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})

export default {
  name: 'ComplexTable',
  components: { Pagination },
  directives: { waves },
  filters: {
    statusFilter(status) {
      const statusMap = {
        published: 'success',
        draft: 'info',
        deleted: 'danger'
      }
      return statusMap[status]
    },
    typeFilter(type) {
      return calendarTypeKeyValue[type]
    }
  },
  data() {
    return {
      tableKey: 0,
      list: null,
      total: 0,
      listLoading: true,
      listQuery: {
        page: 1,
        limit: 10,
        zone_name: undefined,
        sort: '+id'
      },
      search_temp: {
        zone_name: ''
      },
      page: 1,
      zonenamelist: '',
      dnstypelist: '',
      importanceOptions: [1, 2, 3],
      status_swicth,
      calendarTypeOptions,
      sortOptions: [{ label: 'ID Ascending', key: '+id' }, { label: 'ID Descending', key: '-id' }],
      statusOptions: ['published', 'draft', 'deleted'],
      showReviewer: false,
      temp: {
        zone_name: '',
        record_name: '',
        record_content: '',
        record_type: '',
        internet_type: '',
        record_ttl: '',
        dns_type: ''
      },
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: {
        update: 'Edit',
        create: 'Create'
      },
      dialogPvVisible: false,
      pvData: [],
      rules: {
        record: [{ required: true, message: 'record is required', trigger: 'blur' }]
      },
      downloadLoading: false
    }
  },
  created() {
    this.getList()
    this.getZonename()
    this.getDnstype()
  },
  methods: {
    getList() {
      this.listLoading = true
      // fetchList(currentPage).then(response => {
      fetchList({ 'zonename': this.search_temp.zone_name, 'page': this.page }).then(response => {
        debugger
        console.log(response.msg)
        // this.list = response.data.items
        this.list = response.msg.results
        this.total = response.msg.count

        // Just to simulate the time of the request
        setTimeout(() => {
          this.listLoading = false
        }, 1.5 * 1000)
      })
    },
    getZonename() {
      fetchZone().then(response => {
        debugger
        console.log(response.msg)
        var res = response.msg.results
        if (res.length > 0) {
          this.zonenamelist = response.msg.results
        }
      })
    },
    getDnstype() {
      fetchDnstype().then(response => {
        debugger
        console.log(response.msg)
        var res = response.msg.results
        if (res.length > 0) {
          this.dnstypelist = response.msg.results
        }
        console.log(this.dnstypelist)
      })
    },
    handleFilter() {
      this.page = 1
      this.getList()
    },
    handleModifyStatus(row, status) {
      this.$message({
        message: '操作Success',
        type: 'success'
      })
      row.status = status
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    sortChange(data) {
      const { prop, order } = data
      if (prop === 'id') {
        this.sortByID(order)
      }
    },
    sortByID(order) {
      if (order === 'ascending') {
        this.listQuery.sort = '+id'
      } else {
        this.listQuery.sort = '-id'
      }
      this.handleFilter()
    },
    resetTemp() {
      this.temp = {
        zone_name: '',
        record_name: '',
        record_content: '',
        record_type: '',
        internet_type: '',
        record_ttl: '',
        dns_type: ''
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
          debugger
          console.log('hhhhhhhhhh')
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
      var dnsname = row.dns_type.id
      var zonename = row.zone_name.id
      this.temp = Object.assign({}, row) // copy obj
      delete this.temp.dns_type
      delete this.temp.zone_name
      this.$set(this.temp, 'dns_type', dnsname)
      this.$set(this.temp, 'zone_name', zonename)
      this.dialogStatus = 'update'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    modifyData() {
      if (this.dialogStatus === 'delete') {
        this.deleteData()
      } else {
        this.updateData()
      }
    },
    updateData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          debugger
          console.log(this.temp)
          const tempData = Object.assign({}, this.temp)
          console.log(tempData)
          console.log(tempData)
          var id = tempData.id
          delete tempData.id
          update(tempData, id).then(() => {
            debugger
            for (const v of this.list) {
              console.log(v.id)
              console.log(this.temp.id)
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
      this.temp = Object.assign({}, row) // copy obj
      this.dialogStatus = 'delete'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
      debugger
      console.log('handeldelete')
      console.log(row)
      this.index = this.list.indexOf(row)
      // this.list.splice(index, 1)
    },
    deleteData() {
      this.list.splice(this.index, 1)
      this.index = -1
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          debugger
          console.log(this.temp)
          const tempData = Object.assign({}, this.temp)
          console.log(tempData)
          console.log(tempData)
          var id = tempData.id
          deleteid(id).then(() => {
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
              message: 'delete Successfully',
              type: 'success',
              duration: 2000
            })
          })
        }
      })
    },
    handleGenerate() {
      generateConfig({ 'zonename': this.search_temp.zone_name }).then(response => {
        this.dialogFormVisible = false
        this.$notify({
          title: 'Success',
          message: 'generate Successfully',
          type: 'success',
          duration: 2000
        })
      })
    },
    handleFetchPv(pv) {
      fetchOne(pv).then(response => {
        this.pvData = response.data.pvData
        this.dialogPvVisible = true
      })
    },
    formatJson(filterVal, jsonData) {
      return jsonData.map(v => filterVal.map(j => {
        if (j === 'timestamp') {
          return parseTime(v[j])
        } else {
          return v[j]
        }
      }))
    }
  }
}
</script>
