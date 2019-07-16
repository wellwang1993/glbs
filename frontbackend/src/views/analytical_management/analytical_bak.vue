<template>
  <div class="app-container">
    <div class="filter-container" :model="search_temp">
      <el-input v-model="search_temp.nameid" placeholder="nameid" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
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
      <el-table-column label="nameid_name" width="350px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.nameid_name }}</span>
        </template>
      </el-table-column>
      <el-table-column label="zonename" width="350px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.zone_type.zone_name }}</span>
        </template>
      </el-table-column>
      <el-table-column label="dns_name" width="350px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.dns_type.dns_name }}</span>
        </template>
      </el-table-column>

      <el-table-column label="nameid_policy" width="350px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.nameid_policy.policy_name }}</span>
        </template>
      </el-table-column>
      <el-table-column label="nameid_status" width="350px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.nameid_status }}</span>
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
          <el-button v-if="row.status!='deleted'" size="mini" type="danger" @click="handleConfig(row.id)">
            Config
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="page" :limit.sync="listQuery.limit" @pagination="getList" />

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible">
      <el-form ref="dataForm" :model="temp" label-position="left" label-width="120px" style="width: 400px; margin-left:50px;">
        <el-form-item label="nameid_name" prop="record">
          <el-input v-model="temp.nameid_name" />
        </el-form-item>
        <el-form-item label="Zonename" prop="record">
          <el-select v-model="temp.zone_type" class="filter-item" placeholder="Please select">
            <el-option v-for="item in zonenamelist" :key="item.zone_name" :label="item.zone_name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="Nameidpolicy" prop="record">
          <el-select v-model="temp.nameid_policy" class="filter-item" placeholder="Please select">
            <el-option v-for="item in policylist" :key="item.policy_name" :label="item.policy_name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="Dnstype" prop="record">
          <el-select v-model="temp.dns_type" class="filter-item" placeholder="Please select">
            <el-option v-for="item in dnstypelist" :key="item.dns_name" :label="item.dns_name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="nameid_status" prop="record">
          <el-select v-model="temp.nameid_status" class="filter-item" placeholder="Please select">
            <el-option v-for="item in status_swicth" :key="item" :label="item" :value="item" />
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

    <el-dialog :title="textMap[addviewdialogStatus]" :visible.sync="addviewdialogFormVisible">
      <el-form ref="dataViewForm" :model="view_temp" label-position="left" label-width="200px" style="width: 400px; margin-left:50px;">
        <v-distpicker @getid_add_fun="recvfromchild_add_fun"></v-distpicker>
        <el-form-item label="nameid_resolve_type" prop="record">
          <el-select v-model="view_temp.nameid_resolve_type" class="filter-item" placeholder="Please select">
            <el-option v-for="item in resolve_type_choice" :key="item" :label="item" :value="item" />
          </el-select>
        </el-form-item>
        <el-form-item label="nameid_preferred" prop="record">
          <el-select v-model="view_temp.nameid_preferred" class="filter-item" placeholder="Please select">
            <el-option v-for="item in preferred_type_choice" :key="item" :label="item" :value="item" />
          </el-select>
        </el-form-item>
        <el-form-item label="nameid_max_ip" prop="record">
          <el-input v-model="view_temp.nameid_max_ip" />
        </el-form-item>
        <el-form-item label="nameid_ttl" prop="record">
          <el-input v-model="view_temp.nameid_ttl" />
        </el-form-item>
        <el-form-item label="nameid_status" prop="record">
          <el-select v-model="view_temp.nameid_status" class="filter-item" placeholder="Please select">
            <el-option v-for="item in status_swicth" :key="item" :label="item" :value="item" />
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="addviewdialogFormVisible = false">
          Cancel
        </el-button>
        <el-button type="primary" @click="addviewdialogStatus==='create'?createViewData():modifyViewData()">
          Confirm
        </el-button>
      </div>
    </el-dialog>
    <el-dialog :title="textMap[ipratiodialogStatus]" :visible.sync="ipratiodialogFormVisible">
      <el-form ref="dataViewIpForm" :model="ipratio_temp" label-position="left" label-width="200px" style="width: 400px; margin-left:50px;">
        <el-form-item label="vipaddress" prop="record">
          <el-input v-model="ipratio_temp.nameid_device_id.vip_address" />
        </el-form-item>
        <el-form-item label="ratio" prop="record">
          <el-input v-model="ipratio_temp.nameid_device_ratio" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="ipratiodialogFormVisible = false">
          Cancel
        </el-button>
        <el-button type="primary" @click="ipratiodialogStatus==='update'?updateViewIpData():deleteViewIpData()">
          Confirm
        </el-button>
      </div>
    </el-dialog>

    <el-dialog :title="textMap[cnameratiodialogStatus]" :visible.sync="cnameratiodialogFormVisible">
      <el-form ref="dataViewCnameForm" :model="cnameratio_temp" label-position="left" label-width="200px" style="width: 400px; margin-left:50px;">
        <el-form-item label="cname" prop="record">
          <el-input v-model="cnameratio_temp.nameid_cname_id.nameid_cname" />
        </el-form-item>
        <el-form-item label="ratio" prop="record">
          <el-input v-model="cnameratio_temp.nameid_cname_ratio" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="cnameratiodialogFormVisible = false">
          Cancel
        </el-button>
        <el-button type="primary" @click="cnameratiodialogStatus==='update'?updateViewCnameData():deleteViewCnameData()">
          Confirm
        </el-button>
      </div>
    </el-dialog>

    <el-dialog :title="textMap[addipdialogStatus]" :visible.sync="addipdialogFormVisible">
      <div class="filter-container" :model="all_ip_temp">
        <el-input v-model="all_ip_temp.country" placeholder="country" style="width: 200px;" class="filter-item" @keyup.enter.native="handleIpFilter" />
        <el-input v-model="all_ip_temp.isp" placeholder="isp" style="width: 200px;" class="filter-item" @keyup.enter.native="handleIpFilter" />
        <el-input v-model="all_ip_temp.region" placeholder="region" style="width: 200px;" class="filter-item" @keyup.enter.native="handleIpFilter" />
        <el-input v-model="all_ip_temp.province" placeholder="province" style="width: 200px;" class="filter-item" @keyup.enter.native="handleIpFilter" />
        <el-input v-model="all_ip_temp.city" placeholder="city" style="width: 200px;" class="filter-item" @keyup.enter.native="handleIpFilter" />
        <el-input v-model="all_ip_temp.nodeid" placeholder="nodeid" style="width: 200px;" class="filter-item" @keyup.enter.native="handleIpFilter" />
        <el-input v-model="all_ip_temp.ip" placeholder="ip" style="width: 200px;" class="filter-item" @keyup.enter.native="handleIpFilter" />
        <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleIpFilter">
          Search
        </el-button>
      </div>
      <el-table
        ref="viewtable"
        :key="tableKeys"
        v-loading="iplistLoading"
        :data="iplist"
        border
        fit
        highlight-current-row
        style="width: 100%;"
        @sort-change="sortChange"
      >
        <el-table-column label="ID">
          <template slot-scope="scope">
            <span>{{ scope.row.id }}</span>
          </template>
        </el-table-column>
        <el-table-column label="vip_address">
          <template slot-scope="scope">
            <span>{{ scope.row.vip_address }}</span>
          </template>
        </el-table-column>
        <el-table-column label="node_id">
          <template slot-scope="scope">
            <span>{{ scope.row.node_id }}</span>
          </template>
        </el-table-column>
        <el-table-column label="node_country">
          <template slot-scope="scope">
            <span>{{ scope.row.node_country }}</span>
          </template>
        </el-table-column>
        <el-table-column label="node_isp">
          <template slot-scope="scope">
            <span>{{ scope.row.node_isp }}</span>
          </template>
        </el-table-column>
        <el-table-column label="node_region">
          <template slot-scope="scope">
            <span>{{ scope.row.node_region }}</span>
          </template>
        </el-table-column>
        <el-table-column label="node_province">
          <template slot-scope="scope">
            <span>{{ scope.row.node_province }}</span>
          </template>
        </el-table-column>
        <el-table-column label="node_city">
          <template slot-scope="scope">
            <span>{{ scope.row.node_city }}</span>
          </template>
        </el-table-column>
        <el-table-column label="vip_status">
          <template slot-scope="scope">
            <span>{{ scope.row.vip_status }}</span>
          </template>
        </el-table-column>
        <el-table-column label="vip_bandwidth">
          <template slot-scope="scope">
            <span>{{ scope.row.vip_bandwidth }}</span>
          </template>
        </el-table-column>
        <el-table-column label="vip_enable_switch">
          <template slot-scope="scope">
            <span>{{ scope.row.vip_enable_switch }}</span>
          </template>
        </el-table-column>
        <el-table-column label="Actions" align="center" width="300px" class-name="small-padding fixed-width">
          <template slot-scope="{row}">
            <el-button type="primary" size="mini" @click="handleIpAdd(row)">
              add
            </el-button>
            <el-button v-if="row.status!='deleted'" size="mini" type="danger" @click="handleIpCancel(row)">
              cancel
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <div slot="footer" class="dialog-footer">
        <el-button @click="addipdialogFormVisible = false">
          Cancel
        </el-button>
        <el-button type="primary" @click="createIpData()">
          Confirm
        </el-button>
      </div>
      <pagination v-show="iptotal>0" :total="iptotal" :page.sync="ippage" :limit.sync="listQuery.limit" @pagination="handleViewIpCreate" />
    </el-dialog>

    <el-dialog :title="textMap[addcnamedialogStatus]" :visible.sync="addcnamedialogFormVisible">
      <div class="filter-container" :model="all_cname_temp">
        <el-input v-model="all_cname_temp.nameid_cname" placeholder="nameid_cname" style="width: 200px;" class="filter-item" @keyup.enter.native="handleCnameFilter" />
        <el-input v-model="all_cname_temp.nameid_owner" placeholder="nameid_owner" style="width: 200px;" class="filter-item" @keyup.enter.native="handleCnameFilter" />
        <el-input v-model="all_cname_temp.nameid_supplier" placeholder="nameid_supplier" style="width: 200px;" class="filter-item" @keyup.enter.native="handleCnameFilter" />
        <el-input v-model="all_cname_temp.nameid_business" placeholder="nameid_business" style="width: 200px;" class="filter-item" @keyup.enter.native="handleCnameFilter" />
        <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleCnameFilter">
          Search
        </el-button>
      </div>
      <el-table
        ref="viewtable"
        :key="tableKeys"
        v-loading="cnamelistLoading"
        :data="cnamelist"
        border
        fit
        highlight-current-row
        style="width: 100%;"
        @sort-change="sortChange"
      >
        <el-table-column label="ID">
          <template slot-scope="scope">
            <span>{{ scope.row.id }}</span>
          </template>
        </el-table-column>
        <el-table-column label="nameid_cname">
          <template slot-scope="scope">
            <span>{{ scope.row.nameid_cname }}</span>
          </template>
        </el-table-column>
        <el-table-column label="nameid_owner">
          <template slot-scope="scope">
            <span>{{ scope.row.nameid_owner }}</span>
          </template>
        </el-table-column>
        <el-table-column label="nameid_supplier">
          <template slot-scope="scope">
            <span>{{ scope.row.nameid_supplier }}</span>
          </template>
        </el-table-column>
        <el-table-column label="nameid_business">
          <template slot-scope="scope">
            <span>{{ scope.row.nameid_business }}</span>
          </template>
        </el-table-column>
        <el-table-column label="Actions" align="center" width="300px" class-name="small-padding fixed-width">
          <template slot-scope="{row}">
            <el-button type="primary" size="mini" @click="handleCnameAdd(row)">
              add
            </el-button>
            <el-button v-if="row.status!='deleted'" size="mini" type="danger" @click="handleCnameCancel(row)">
              cancel
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <div slot="footer" class="dialog-footer">
        <el-button @click="addipdialogFormVisible = false">
          Cancel
        </el-button>
        <el-button type="primary" @click="createCnameData()">
          Confirm
        </el-button>
      </div>
      <pagination v-show="iptotal>0" :total="iptotal" :page.sync="ippage" :limit.sync="listQuery.limit" @pagination="handleViewIpCreate" />
    </el-dialog>

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="viewdialogFormVisible">
      <div class="filter-container" :model="search_temp">
        <v-distpicker @getid="recvfromchild"></v-distpicker>
        <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleViewCreate">
          Add
        </el-button>
      </div>
      <el-table
        ref="viewtable"
        :key="tableKeys"
        v-loading="viewlistLoading"
        :data="viewlist"
        border
        fit
        highlight-current-row
        style="width: 100%;"
        @sort-change="sortChange"
      >
        <el-table-column label="ID">
          <template slot-scope="scope">
            <span>{{ scope.row.id }}</span>
          </template>
        </el-table-column>
        <el-table-column label="nameid">
          <template slot-scope="scope">
            <span>{{ scope.row.nameid_id.nameid_name }}</span>
          </template>
        </el-table-column>
        <el-table-column label="view_default">
          <template slot-scope="scope">
            <span>{{ scope.row.nameid_view_id.view_default }}</span>
          </template>
        </el-table-column>
        <el-table-column label="view_country">
          <template slot-scope="scope">
            <span>{{ scope.row.nameid_view_id.view_country }}</span>
          </template>
        </el-table-column>
        <el-table-column label="view_isp">
          <template slot-scope="scope">
            <span>{{ scope.row.nameid_view_id.view_isp }}</span>
          </template>
        </el-table-column>
        <el-table-column label="view_region">
          <template slot-scope="scope">
            <span>{{ scope.row.nameid_view_id.view_region }}</span>
          </template>
        </el-table-column>
        <el-table-column label="view_province">
          <template slot-scope="scope">
            <span>{{ scope.row.nameid_view_id.view_province }}</span>
          </template>
        </el-table-column>
        <el-table-column label="view_city">
          <template slot-scope="scope">
            <span>{{ scope.row.nameid_view_id.view_city }}</span>
          </template>
        </el-table-column>
        <el-table-column label="nameid_resolve_type">
          <template slot-scope="scope">
            <span>{{ scope.row.nameid_resolve_type }}</span>
          </template>
        </el-table-column>
        <el-table-column label="nameid_max_ip">
          <template slot-scope="scope">
            <span>{{ scope.row.nameid_max_ip }}</span>
          </template>
        </el-table-column>
        <el-table-column label="nameid_preferred">
          <template slot-scope="scope">
            <span>{{ scope.row.nameid_preferred }}</span>
          </template>
        </el-table-column>
        <el-table-column label="nameid_status">
          <template slot-scope="scope">
            <span>{{ scope.row.nameid_status }}</span>
          </template>
        </el-table-column>
        <el-table-column label="nameid_ttl">
          <template slot-scope="scope">
            <span>{{ scope.row.nameid_ttl }}</span>
          </template>
        </el-table-column>
        <el-table-column label="Actions" align="center" width="400px" class-name="small-padding fixed-width">
          <template slot-scope="{row}">
            <el-button type="primary" size="mini" @click="handleViewUpdate(row)">
              Edit
            </el-button>
            <el-button v-if="row.status!='deleted'" size="mini" type="danger" @click="handleViewDelete(row)">
              Delete
            </el-button>
            <el-button v-if="row.status!='deleted'" size="mini" type="danger" @click="handleViewConfig(row)">
              ConfigIp
            </el-button>
            <el-button v-if="row.status!='deleted'" size="mini" type="danger" @click="handleViewCnameConfig(row)">
              ConfigCname
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <div slot="footer" class="dialog-footer">
        <el-button @click="viewdialogFormVisible = false">
          Cancel
        </el-button>
        <el-button type="primary" @click="dialogStatus==='create'?createData():modifyData()">
          Confirm
        </el-button>
      </div>
    </el-dialog>

    <el-dialog :title="textMap[addviewipdialogStatus]" :visible.sync="addviewipdialogFormVisible">
      <div class="filter-container" :model="ip_temp">
        <el-input v-model="ip_temp.ip" placeholder="vip" style="width: 200px;" class="filter-item" @keyup.enter.native="handleViewIpFilter" />
        <el-input v-model="ip_temp.node" placeholder="node" style="width: 200px;" class="filter-item" @keyup.enter.native="handleViewIpFilter" />
        <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleViewIpFilter">
          Search
        </el-button>
        <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleViewIpCreate">
          Add
        </el-button>
      </div>
      <el-table
        ref="viewiptable"
        :key="tableKeys"
        v-loading="viewiplistLoading"
        :data="viewiplist"
        border
        fit
        highlight-current-row
        style="width: 100%;"
        @sort-change="sortChange"
      >
        <el-table-column label="ID">
          <template slot-scope="scope">
            <span>{{ scope.row.id }}</span>
          </template>
        </el-table-column>
        <el-table-column label="nameid">
          <template slot-scope="scope">
            <span>{{ scope.row.nameid_id.nameid_name }}</span>
          </template>
        </el-table-column>
        <el-table-column label="view_default">
          <template slot-scope="scope">
            <span>{{ scope.row.nameid_view_id.view_default }}</span>
          </template>
        </el-table-column>
        <el-table-column label="view_country">
          <template slot-scope="scope">
            <span>{{ scope.row.nameid_view_id.view_country }}</span>
          </template>
        </el-table-column>
        <el-table-column label="view_isp">
          <template slot-scope="scope">
            <span>{{ scope.row.nameid_view_id.view_isp }}</span>
          </template>
        </el-table-column>
        <el-table-column label="view_region">
          <template slot-scope="scope">
            <span>{{ scope.row.nameid_view_id.view_region }}</span>
          </template>
        </el-table-column>
        <el-table-column label="view_province">
          <template slot-scope="scope">
            <span>{{ scope.row.nameid_view_id.view_province }}</span>
          </template>
        </el-table-column>
        <el-table-column label="view_city">
          <template slot-scope="scope">
            <span>{{ scope.row.nameid_view_id.view_city }}</span>
          </template>
        </el-table-column>
        <el-table-column label="nameid_device_id">
          <template slot-scope="scope">
            <span>{{ scope.row.nameid_device_id.vip_address }}</span>
          </template>
        </el-table-column>
        <el-table-column label="nameid_device_ratio">
          <template slot-scope="scope">
            <span>{{ scope.row.nameid_device_ratio }}</span>
          </template>
        </el-table-column>
        <el-table-column label="nameid_device_status">
          <template slot-scope="scope">
            <span>{{ scope.row.nameid_device_status }}</span>
          </template>
        </el-table-column>
        <el-table-column label="Actions" align="center" width="300px" class-name="small-padding fixed-width">
          <template slot-scope="{row}">
            <el-button type="primary" size="mini" @click="handleViewIpUpdate(row)">
              Edit
            </el-button>
            <el-button v-if="row.status!='deleted'" size="mini" type="danger" @click="handleViewIpDelete(row)">
              Delete
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <div slot="footer" class="dialog-footer">
        <el-button @click="addviewipdialogFormVisible = false">
          Cancel
        </el-button>
        <el-button type="primary" @click="ipratiodialogStatus==='create'?createData():modifyData()">
          Confirm
        </el-button>
      </div>
    </el-dialog>

    <el-dialog :title="textMap[addviewcnamedialogStatus]" :visible.sync="addviewcnamedialogFormVisible">
      <div class="filter-container" :model="cname_temp">
        <el-input v-model="cname_temp.cname" placeholder="cname" style="width: 200px;" class="filter-item" @keyup.enter.native="handleViewCnameFilter" />
        <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleViewCnameFilter">
          Search
        </el-button>
        <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleViewCnameCreate">
          Add
        </el-button>
      </div>
      <el-table
        ref="viewiptable"
        :key="tableKeys"
        v-loading="viewcnamelistLoading"
        :data="viewcnamelist"
        border
        fit
        highlight-current-row
        style="width: 100%;"
        @sort-change="sortChange"
      >
        <el-table-column label="ID">
          <template slot-scope="scope">
            <span>{{ scope.row.id }}</span>
          </template>
        </el-table-column>
        <el-table-column label="nameid">
          <template slot-scope="scope">
            <span>{{ scope.row.nameid_id.nameid_name }}</span>
          </template>
        </el-table-column>
        <el-table-column label="view_default">
          <template slot-scope="scope">
            <span>{{ scope.row.nameid_view_id.view_default }}</span>
          </template>
        </el-table-column>
        <el-table-column label="view_country">
          <template slot-scope="scope">
            <span>{{ scope.row.nameid_view_id.view_country }}</span>
          </template>
        </el-table-column>
        <el-table-column label="view_isp">
          <template slot-scope="scope">
            <span>{{ scope.row.nameid_view_id.view_isp }}</span>
          </template>
        </el-table-column>
        <el-table-column label="view_region">
          <template slot-scope="scope">
            <span>{{ scope.row.nameid_view_id.view_region }}</span>
          </template>
        </el-table-column>
        <el-table-column label="view_province">
          <template slot-scope="scope">
            <span>{{ scope.row.nameid_view_id.view_province }}</span>
          </template>
        </el-table-column>
        <el-table-column label="view_city">
          <template slot-scope="scope">
            <span>{{ scope.row.nameid_view_id.view_city }}</span>
          </template>
        </el-table-column>
        <el-table-column label="nameid_cname_id">
          <template slot-scope="scope">
            <span>{{ scope.row.nameid_cname_id.nameid_cname }}</span>
          </template>
        </el-table-column>
        <el-table-column label="nameid_cname_ratio">
          <template slot-scope="scope">
            <span>{{ scope.row.nameid_cname_ratio }}</span>
          </template>
        </el-table-column>
        <el-table-column label="nameid_cname_status">
          <template slot-scope="scope">
            <span>{{ scope.row.nameid_cname_status }}</span>
          </template>
        </el-table-column>
        <el-table-column label="Actions" align="center" width="300px" class-name="small-padding fixed-width">
          <template slot-scope="{row}">
            <el-button type="primary" size="mini" @click="handleViewCnameUpdate(row)">
              Edit
            </el-button>
            <el-button v-if="row.status!='deleted'" size="mini" type="danger" @click="handleViewCnameDelete(row)">
              Delete
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <div slot="footer" class="dialog-footer">
        <el-button @click="addviewcnamedialogFormVisible = false">
          Cancel
        </el-button>
        <el-button type="primary" @click="ipratiodialogStatus==='create'?createData():modifyData()">
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
import { fetchIpList, fetchViewIpList, fetchCnameList, fetchViewCnameList, fetchSpecialView, fetchView, generateConfig, fetchDnstype, fetchZone, fetchNameidpolicy, deleteid, fetchList, fetchOne, create, update, createview, updateview, updateviewip, updateviewcname, deleteviewid, deleteviewipid, deleteviewcnameid, createviewip, createviewcname } from '@/api/analytical'
import waves from '@/directive/waves' // waves directive
import { parseTime } from '@/utils'
import Pagination from '@/components/Pagination' // secondary package based on el-pagination
import VDistpicker from '@/v-distpicker'
// import VDistpicker from 'v-distpicker'
import './directives.js'
const calendarTypeOptions = [
  { key: 'CN', display_name: 'China' },
  { key: 'US', display_name: 'USA' },
  { key: 'JP', display_name: 'Japan' },
  { key: 'EU', display_name: 'Eurozone' }
]
const status_swicth = ['enable', 'disable']
const resolve_type_choice = ['cname', 'a', 'aaaa']
const preferred_type_choice = ['ratio', 'rr']
// arr to obj, such as { CN : "China", US : "USA" }
const calendarTypeKeyValue = calendarTypeOptions.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})

export default {
  name: 'ComplexTable',
  components: { Pagination, VDistpicker },
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
      row: '',
      tableKey: 0,
      tableKeys: 0,
      list: null,
      iplist: null,
      cnamelist: null,
      viewlist: null,
      viewiplist: null,
      viewcnamelist: null,
      iplist_temp: [],
      cnamelist_temp: [],
      listLoading: true,
      viewlistLoading: true,
      viewiplistLoading: true,
      viewcnamelistLoading: true,
      iplistLoading: true,
      cnamelistLoading: true,
      total: 0,
      iptotal: 0,
      cnametotal: 0,
      viewtotal: 0,
      viewiptotal: 0,
      viewcnametotal: 0,
      viewid: -1,
      add_viewid: -1,
      nameid: -1,
      listQuery: {
        page: 1,
        limit: 10,
        zone_name: undefined,
        sort: '+id'
      },
      search_temp: {
        nameid: ''
      },
      ip_temp: {
        ip: '',
        node: ''
      },
      cname_temp: {
        cname: ''
      },
      ipratio_temp: {
        nameid_device_id: '',
        nameid_device_ratio: ''
      },
      cnameratio_temp: {
        nameid_cname_id: '',
        nameid_cname_ratio: ''
      },
      all_ip_temp: {
        country: '',
        isp: '',
        region: '',
        province: '',
        city: '',
        ip: '',
        node: ''
      },
      all_cname_temp: {
        nameid_cname: '',
        nameid_owner: '',
        nameid_supplier: '',
        nameid_business: ''
      },
      view_temp: {
        nameid_id: '',
        nameid_view_id: '',
        nameid_resolve_type: '',
        nameid_max_ip: '',
        nameid_preferred: '',
        nameid_status: '',
        nameid_ttl: ''
      },
      page: 1,
      ippage: 1,
      cnamepage: 1,
      zonenamelist: '',
      dnstypelist: '',
      policylist: '',
      importanceOptions: [1, 2, 3],
      status_swicth,
      resolve_type_choice,
      preferred_type_choice,
      calendarTypeOptions,
      sortOptions: [{ label: 'ID Ascending', key: '+id' }, { label: 'ID Descending', key: '-id' }],
      statusOptions: ['published', 'draft', 'deleted'],
      showReviewer: false,
      temp: {
        nameid_name: '',
        zone_type: '',
        dns_type: '',
        nameid_status: '',
        nameid_policy: ''
      },
      dialogFormVisible: false,
      viewdialogFormVisible: false,
      addviewdialogFormVisible: false,
      addviewipdialogFormVisible: false,
      addviewcnamedialogFormVisible: false,
      addipdialogFormVisible: false,
      addcnamedialogFormVisible: false,
      ipratiodialogFormVisible: false,
      cnameratiodialogFormVisible: false,
      dialogStatus: '',
      viewdialogStatus: '',
      addviewdialogStatus: '',
      addviewipdialogStatus: '',
      addviewcnamedialogStatus: '',
      addipdialogStatus: '',
      addcnamedialogStatus: '',
      ipratiodialogStatus: '',
      cnameratiodialogStatus: '',
      textMap: {
        update: 'Edit',
        create: 'Create',
        configview: 'Configview',
        configviewip: 'Configviewip',
        configviewcname: 'Configviewcname'
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
    this.getNameidpolicy()
  },
  methods: {
    recvfromchild_add_fun(data) {
      this.add_viewid = data
    },
    recvfromchild(data) {
      this.viewid = data
      fetchSpecialView({ 'nameid': this.nameid, 'viewid': this.viewid }).then(response => {
        this.viewdialogFormVisible = true
        // debugger
        console.log(response.msg)
        // this.list = response.data.items
        this.viewlist = response.msg.results
        this.viewtotal = response.msg.count

        // Just to simulate the time of the request
        setTimeout(() => {
          this.viewlistLoading = false
        }, 1.5 * 1000)
      })
    },
    onSelected(data) {
      debugger
      console.log(data)
      console.log(data.id)
      this.select.province = data.province
    },
    getList() {
      this.listLoading = true
      // fetchList(currentPage).then(response => {
      fetchList({ 'nameid': this.search_temp.nameid, 'page': this.page }).then(response => {
        // debugger
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
    getViewIpList() {
      this.viewiplistLoading = true
      fetchViewIpList({ 'nameid': this.nameid_view_ip, 'viewid': this.viewid_view_ip, 'nodeid': this.ip_temp.node, 'ip': this.ip_temp.ip, 'page': this.page }).then(response => {
        debugger
        console.log(response.msg)
        // this.list = response.data.items
        this.viewiplist = response.msg.results
        this.viewiptotal = response.msg.count
        console.log(this.viewiplist)

        // Just to simulate the time of the request
        setTimeout(() => {
          this.viewiplistLoading = false
        }, 1.5 * 1000)
      })
    },
    getViewCnameList() {
      this.viewcnamelistLoading = true
      fetchViewCnameList({ 'nameid': this.nameid_view_ip, 'viewid': this.viewid_view_ip, 'cname': this.cname_temp.cname, 'page': this.cnamepage }).then(response => {
        debugger
        console.log(response.msg)
        // this.list = response.data.items
        this.viewcnamelist = response.msg.results
        this.viewcnametotal = response.msg.count
        console.log(this.viewiplist)

        // Just to simulate the time of the request
        setTimeout(() => {
          this.viewcnamelistLoading = false
        }, 1.5 * 1000)
      })
    },
    getZonename() {
      fetchZone().then(response => {
        // debugger
        console.log(response.msg)
        var res = response.msg.results
        if (res.length > 0) {
          this.zonenamelist = response.msg.results
        }
      })
    },
    getDnstype() {
      fetchDnstype().then(response => {
        // debugger
        console.log(response.msg)
        var res = response.msg.results
        if (res.length > 0) {
          this.dnstypelist = response.msg.results
        }
        console.log(this.dnstypelist)
      })
    },
    getNameidpolicy() {
      fetchNameidpolicy().then(response => {
        // debugger
        console.log(response.msg)
        var res = response.msg.results
        if (res.length > 0) {
          this.policylist = response.msg.results
        }
        console.log(this.policylist)
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
    handleCnameAdd(row) {
      this.cnamelist_temp.push(row.id)
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
    handleCnameCancel(row) {
      var index = this.cnamelist_temp.indexOf(row.id)
      if (index !== -1) {
        this.cnamelist_temp.splice(index, 1)
      }
      this.$notify({
        title: 'Success',
        message: 'Cancel Successfully',
        type: 'success',
        duration: 2000
      })
    },
    handleFilter() {
      this.page = 1
      this.getList()
    },
    handleViewIpFilter() {
      this.page = 1
      this.getViewIpList()
    },
    handleViewCnameFilter() {
      this.cnamepage = 1
      this.getViewCnameList()
    },
    handleIpFilter() {
      this.ippage = 1
      this.handleViewIpCreate()
    },
    handleCnameFilter() {
      this.cnamepage = 1
      this.handleViewCnameCreate()
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
        nameid_name: '',
        zone_type: '',
        dns_type: '',
        nameid_status: '',
        nameid_policy: ''
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
    handleViewCreate() {
      this.resetTemp()
      this.addviewdialogStatus = 'create'
      this.addviewdialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataViewForm'].clearValidate()
      })
    },
    handleViewIpCreate() {
      this.resetTemp()
      this.addipdialogStatus = 'create'
      this.iplistLoading = true
      fetchIpList({ 'country': this.all_ip_temp.country, 'isp': this.all_ip_temp.isp, 'region': this.all_ip_temp.region, 'province': this.all_ip_temp.province, 'city': this.all_ip_temp.city, 'nodeid': this.all_ip_temp.nodeid, 'ip': this.all_ip_temp.ip, 'page': this.ippage }).then(response => {
        console.log('uuuuuuuuuu')
        this.addipdialogFormVisible = true
        console.log(response.msg)
        // this.list = response.data.items
        this.iplist = response.msg.results
        this.iptotal = response.msg.count

        // Just to simulate the time of the request
        setTimeout(() => {
          this.iplistLoading = false
        }, 1.5 * 1000)
      })
    },
    handleViewCnameCreate() {
      this.resetTemp()
      this.addcnamedialogStatus = 'create'
      this.cnamelistLoading = true
      fetchCnameList({ 'cname': this.all_cname_temp.nameid_cname, 'operator': this.all_cname_temp.nameid_owner, 'supplier': this.all_cname_temp.nameid_supplier, 'business': this.all_cname_temp.nameid_business, 'page': this.ippage }).then(response => {
        console.log('uuuuuuuuuu')
        this.addcnamedialogFormVisible = true
        console.log(response.msg)
        // this.list = response.data.items
        this.cnamelist = response.msg.results
        this.cnametotal = response.msg.count

        // Just to simulate the time of the request
        setTimeout(() => {
          this.cnamelistLoading = false
        }, 1.5 * 1000)
      })
    },
    createData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          // debugger
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
    createViewData() {
      debugger
      this.view_temp.nameid_id = this.nameid
      this.view_temp.nameid_view_id = this.add_viewid
      console.log(this.view_temp)
      this.$refs['dataViewForm'].validate((valid) => {
        if (valid) {
          // debugger
          console.log('hhhhhhhhhh')
          createview(this.view_temp).then(() => {
            this.viewlist.push(this.view_temp)
            this.addviewdialogFormVisible = false
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
    createIpData() {
      debugger
      console.log('aaasssss')
      console.log(this.iplist_temp)
      console.log('sssss')
      createviewip({ 'nameid': this.nameid_view_ip, 'viewidinfo': [this.viewid_view_ip], 'devidinfo': this.iplist_temp }).then(() => {
        // this.viewiplist.push()
        this.addipdialogFormVisible = false
        this.$notify({
          title: 'Success',
          message: 'Created Successfully',
          type: 'success',
          duration: 2000
        })
      })
      this.iplist_temp = []
    },
    createCnameData() {
      debugger
      console.log('aaasssss')
      console.log(this.cnamelist_temp)
      console.log('sssss')
      createviewcname({ 'nameid': this.nameid_view_ip, 'viewidinfo': [this.viewid_view_ip], 'cnameinfo': this.cnamelist_temp }).then(() => {
        // this.viewiplist.push()
        this.addcnamedialogFormVisible = false
        this.$notify({
          title: 'Success',
          message: 'Created Successfully',
          type: 'success',
          duration: 2000
        })
      })
      this.cnamelist_temp = []
    },
    handleViewUpdate(row) {
      this.view_temp = Object.assign({}, row) // copy obj
      this.addviewdialogFormVisible = true
      this.addviewdialogStatus = 'update'
      console.log(this.view_temp)
      this.$nextTick(() => {
        this.$refs['dataViewForm'].clearValidate()
      })
    },
    handleViewIpUpdate(row) {
      this.ipratio_temp = Object.assign({}, row) // copy obj
      this.ipratiodialogFormVisible = true
      this.ipratiodialogStatus = 'update'
      console.log(this.ip_temp)
      this.$nextTick(() => {
        this.$refs['dataViewIpForm'].clearValidate()
      })
    },
    handleViewCnameUpdate(row) {
      this.cnameratio_temp = Object.assign({}, row) // copy obj
      this.cnameratiodialogFormVisible = true
      this.cnameratiodialogStatus = 'update'
      console.log(this.ip_temp)
      this.$nextTick(() => {
        this.$refs['dataViewCnameForm'].clearValidate()
      })
    },
    handleUpdate(row) {
      var dnsname = row.dns_type.id
      var zonetype = row.zone_type.id
      var policytype = row.nameid_policy.id
      this.temp = Object.assign({}, row) // copy obj
      delete this.temp.dns_type
      delete this.temp.zone_type
      delete this.temp.nameid_policy
      this.$set(this.temp, 'dns_type', dnsname)
      this.$set(this.temp, 'zone_type', zonetype)
      this.$set(this.temp, 'nameid_policy', policytype)
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
    modifyViewData() {
      if (this.addviewdialogStatus === 'delete') {
        this.addviewdeleteData()
      } else {
        this.addviewupdateData()
      }
    },
    addviewupdateData() {
      this.$refs['dataViewForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.view_temp)
          var id = tempData.id
          var nameid = tempData.nameid_id.id
          var viewid = tempData.nameid_view_id.id
          delete tempData.id
          delete tempData.nameid_id
          delete tempData.nameid_view_id
          this.$set(tempData, 'nameid_id', nameid)
          this.$set(tempData, 'nameid_view_id', viewid)
          debugger
          console.log(tempData)
          updateview(tempData, id).then(() => {
            debugger
            for (const v of this.viewlist) {
              console.log(v)
              console.log(v.id)
              console.log(this.view_temp.id)
              if (v.id === this.view_temp.id) {
                const index = this.viewlist.indexOf(v)
                this.viewlist.splice(index, 1, this.view_temp)
                break
              }
            }
            this.addviewdialogFormVisible = false
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
    updateViewIpData() {
      this.$refs['dataViewIpForm'].validate((valid) => {
        if (valid) {
          debugger
          const tempData = Object.assign({}, this.ipratio_temp)
          console.log(this.ipratio_temp)
          var id = tempData.id
          var nameid = tempData.nameid_id.id
          var viewid = tempData.nameid_view_id.id
          var devid = tempData.nameid_device_id.id
          delete tempData.id
          delete tempData.nameid_id
          delete tempData.nameid_view_id
          delete tempData.nameid_device_id
          this.$set(tempData, 'nameid_id', nameid)
          this.$set(tempData, 'nameid_view_id', viewid)
          this.$set(tempData, 'nameid_device_id', devid)
          console.log(tempData)
          updateviewip(tempData, id).then(() => {
            for (const v of this.viewiplist) {
              if (v.id === this.ipratio_temp.id) {
                const index = this.viewiplist.indexOf(v)
                this.viewiplist.splice(index, 1, this.ipratio_temp)
                break
              }
            }
            this.ipratiodialogFormVisible = false
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
    updateViewCnameData() {
      this.$refs['dataViewCnameForm'].validate((valid) => {
        if (valid) {
          debugger
          const tempData = Object.assign({}, this.cnameratio_temp)
          console.log(this.cnameratio_temp)
          var id = tempData.id
          var nameid = tempData.nameid_id.id
          var viewid = tempData.nameid_view_id.id
          var cnameid = tempData.nameid_cname_id.id
          delete tempData.id
          delete tempData.nameid_id
          delete tempData.nameid_view_id
          delete tempData.nameid_cname_id
          this.$set(tempData, 'nameid_id', nameid)
          this.$set(tempData, 'nameid_view_id', viewid)
          this.$set(tempData, 'nameid_cname_id', cnameid)
          console.log(tempData)
          updateviewcname(tempData, id).then(() => {
            for (const v of this.viewcnamelist) {
              if (v.id === this.cnameratio_temp.id) {
                const index = this.viewcnamelist.indexOf(v)
                this.viewcnamelist.splice(index, 1, this.cnameratio_temp)
                break
              }
            }
            this.cnameratiodialogFormVisible = false
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
    updateData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          // debugger
          console.log(this.temp)
          const tempData = Object.assign({}, this.temp)
          console.log(tempData)
          console.log(tempData)
          var id = tempData.id
          delete tempData.id
          update(tempData, id).then(() => {
            // debugger
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
      var dnsname = row.dns_type.id
      var zonetype = row.zone_type.id
      var policytype = row.nameid_policy.id
      this.temp = Object.assign({}, row) // copy obj
      delete this.temp.dns_type
      delete this.temp.zone_type
      delete this.temp.nameid_policy
      this.$set(this.temp, 'dns_type', dnsname)
      this.$set(this.temp, 'zone_type', zonetype)
      this.$set(this.temp, 'nameid_policy', policytype)
      this.dialogStatus = 'delete'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
      // debugger
      console.log('handeldelete')
      console.log(row)
      this.index = this.list.indexOf(row)
      // this.list.splice(index, 1)
    },
    handleViewDelete(row) {
      this.view_temp = Object.assign({}, row) // copy obj
      this.addviewdialogFormVisible = true
      this.addviewdialogStatus = 'delete'
      debugger
      console.log(this.view_temp)
      this.$nextTick(() => {
        this.$refs['dataViewForm'].clearValidate()
      })
      this.viewindex = this.viewlist.indexOf(row)
    },
    handleViewIpDelete(row) {
      this.ipratio_temp = Object.assign({}, row) // copy obj
      this.ipratiodialogFormVisible = true
      this.ipratiodialogStatus = 'delete'
      debugger
      console.log(this.ipratio_temp)
      this.$nextTick(() => {
        this.$refs['dataViewIpForm'].clearValidate()
      })
      this.viewipindex = this.viewiplist.indexOf(row)
      console.log(this.viewipindex)
    },
    handleViewCnameDelete(row) {
      this.cnameratio_temp = Object.assign({}, row) // copy obj
      this.cnameratiodialogFormVisible = true
      this.cnameratiodialogStatus = 'delete'
      debugger
      console.log(this.cnameratio_temp)
      this.$nextTick(() => {
        this.$refs['dataViewCnameForm'].clearValidate()
      })
      this.viewcnameindex = this.viewcnamelist.indexOf(row)
      console.log(this.viewcnameindex)
    },
    deleteData() {
      this.list.splice(this.index, 1)
      this.index = -1
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          // debugger
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
    addviewdeleteData() {
      this.viewlist.splice(this.viewindex, 1)
      this.viewindex = -1
      this.$refs['dataViewForm'].validate((valid) => {
        if (valid) {
          // debugger
          const tempData = Object.assign({}, this.view_temp)
          console.log(tempData)
          var id = tempData.id
          deleteviewid(id).then(() => {
            for (const v of this.viewlist) {
              if (v.id === this.view_temp.id) {
                const index = this.viewlist.indexOf(v)
                this.viewlist.splice(index, 1, this.view_temp)
                break
              }
            }
            this.addviewdialogFormVisible = false
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
    deleteViewIpData() {
      this.viewiplist.splice(this.viewipindex, 1)
      this.viewipindex = -1
      this.$refs['dataViewIpForm'].validate((valid) => {
        if (valid) {
          // debugger
          const tempData = Object.assign({}, this.ipratio_temp)
          console.log(tempData)
          var id = tempData.id
          deleteviewipid(id).then(() => {
            for (const v of this.viewiplist) {
              if (v.id === this.ipratio_temp.id) {
                const index = this.viewiplist.indexOf(v)
                this.viewiplist.splice(index, 1, this.ipratio_temp)
                break
              }
            }
            this.ipratiodialogFormVisible = false
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
    deleteViewCnameData() {
      this.viewcnamelist.splice(this.viewcnameindex, 1)
      this.viewcnameindex = -1
      this.$refs['dataViewCnameForm'].validate((valid) => {
        if (valid) {
          // debugger
          const tempData = Object.assign({}, this.cnameratio_temp)
          console.log(tempData)
          var id = tempData.id
          deleteviewcnameid(id).then(() => {
            for (const v of this.viewcnamelist) {
              if (v.id === this.cnameratio_temp.id) {
                const index = this.viewcnamelist.indexOf(v)
                this.viewcnamelist.splice(index, 1, this.cnameratio_temp)
                break
              }
            }
            this.cnameratiodialogFormVisible = false
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
    handleConfig(nameid) {
      this.viewlistLoading = true
      this.dialogStatus = 'configview'
      // debugger
      console.log(nameid)
      this.nameid = nameid
      // this.$nextTick(() => {
      // this.$refs['viewtable'].id = 3
      // })
      fetchView({ 'nameid': nameid, 'page': this.page }).then(response => {
        this.viewdialogFormVisible = true
        // debugger
        console.log(response.msg)
        // this.list = response.data.items
        this.viewlist = response.msg.results
        this.viewtotal = response.msg.count

        // Just to simulate the time of the request
        setTimeout(() => {
          this.viewlistLoading = false
        }, 1.5 * 1000)
      })
    },
    handleViewConfig(row) {
      this.viewiplistLoading = true
      this.addviewipdialogStatus = 'configviewip'
      debugger
      console.log(row)
      this.nameid_view_ip = row.nameid_id.id
      this.viewid_view_ip = row.nameid_view_id.id
      fetchViewIpList({ 'nameid': this.nameid_view_ip, 'viewid': this.viewid_view_ip, 'nodeid': this.ip_temp.node, 'ip': this.ip_temp.ip, 'page': this.page }).then(response => {
      // fetchViewIp({ 'nameid': this.nameid_view_ip, 'viewid': this.viewid_view_ip, 'page': this.page }).then(response => {
        console.log('uuuuuuuuuu')
        this.addviewipdialogFormVisible = true
        // debugger
        console.log(response.msg)
        // this.list = response.data.items
        this.viewiplist = response.msg.results
        this.viewiptotal = response.msg.count

        // Just to simulate the time of the request
        setTimeout(() => {
          this.viewiplistLoading = false
        }, 1.5 * 1000)
      })
    },
    handleViewCnameConfig(row) {
      this.viewcnamelistLoading = true
      this.addviewcnamedialogStatus = 'configviewcname'
      debugger
      console.log(row)
      this.nameid_view_ip = row.nameid_id.id
      this.viewid_view_ip = row.nameid_view_id.id
      fetchViewCnameList({ 'nameid': this.nameid_view_ip, 'viewid': this.viewid_view_ip, 'cname': this.cname_temp.cname, 'page': this.page }).then(response => {
        console.log('uuuuuuuuuu')
        this.addviewcnamedialogFormVisible = true
        // debugger
        console.log(response.msg)
        // this.list = response.data.items
        this.viewcnamelist = response.msg.results
        this.viewcnametotal = response.msg.count

        // Just to simulate the time of the request
        setTimeout(() => {
          this.viewcnamelistLoading = false
        }, 1.5 * 1000)
      })
    },
    handleGenerate() {
      generateConfig({ 'zonename': this.search_temp.zone_name }).then(response => {
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
