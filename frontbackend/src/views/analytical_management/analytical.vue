<template>
  <div class="app-container">
    <div class="filter-container" :model="search_temp">
      <el-input v-model="search_temp.nameid" placeholder="nameid" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        Search
      </el-button>
      <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleCreate">
        Add
      </el-button>
      <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleGenerate">
        Generate
      </el-button>
      <el-button v-if="row.status!='deleted'" size="mini" type="danger" @click="handleCopyName">
        Copyname
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
            <el-button type="primary" size="mini" @click="deleteData(row)">
              Confirm
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>
    <pagination v-show="total>0" :total="total" :page.sync="page" :limit.sync="limit" @pagination="getList" />

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
            <el-option v-for="item in nameid_status_swicth" :key="item" :label="item" :value="item" />
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

    <el-dialog :title="textMap[dialogNameidViewStatus]" :visible.sync="dialogFormNameidViewVisible">
      <el-form ref="dataViewForm" :model="view_temp" label-position="left" label-width="200px" style="width: 400px; margin-left:50px;">
        <v-distpicker @getAddViewId="getNameidViewid"></v-distpicker>
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
        <el-button @click="dialogFormNameidViewVisible = false">
          Cancel
        </el-button>
        <el-button type="primary" @click="createViewData()">
          Confirm
        </el-button>
      </div>
    </el-dialog>

    <el-dialog :title="textMap[dialogNameidViewUpdateStatus]" :visible.sync="dialogFormNameidViewUpdateVisible">
      <el-form ref="dataViewUpdateForm" :model="view_temp" label-position="left" label-width="200px" style="width: 400px; margin-left:50px;">
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
        <el-button @click="dialogFormNameidViewUpdateVisible = false">
          Cancel
        </el-button>
        <el-button type="primary" @click="updateViewData()">
          Confirm
        </el-button>
      </div>
    </el-dialog>
    <el-dialog :title="textMap[dialogViewStatus]" :visible.sync="dialogFormViewVisible">
      <div class="filter-container" :model="search_temp">
        <v-distpicker @getNameidViewList="getSpecialViewList"></v-distpicker>
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
        <el-table-column label="Actions" align="center" width="500px" class-name="small-padding fixed-width">
          <template slot-scope="{row}">
            <el-button type="primary" size="mini" @click="handleViewUpdate(row)">
              Edit
            </el-button>
            <el-button v-if="row.status!='deleted'" size="mini" type="danger" @click="handleViewDelete(row)">
              Delete
            </el-button>
            <el-button v-if="row.status!='deleted'" size="mini" type="danger" @click="handleViewIpConfig(row)">
              ConfigIp
            </el-button>
            <el-button v-if="row.status!='deleted'" size="mini" type="danger" @click="handleViewCnameConfig(row)">
              ConfigCname
            </el-button>
            <el-button v-if="row.status!='deleted'" size="mini" type="danger" @click="GenerateView(row)">
              Generate
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <pagination v-show="viewtotal>0" :total="viewtotal" :page.sync="viewpage" :limit.sync="viewlimit" @pagination="handleConfig(nameid_idx)" />
    </el-dialog>

    <el-dialog :title="textMap[dialogDeleteViewStatus]" :visible.sync="dialogDeleteFormViewVisible">
      <el-table
        ref="viewtable"
        :key="tableKey"
        v-loading="deleteviewLoading"
        :data="deleteviewdata"
        border
        fit
        highlight-current-row
        style="width: 100%;"
        @sort-change="sortChange"
      >
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
        <el-table-column label="Actions" align="center" width="300px" class-name="small-padding fixed-width">
          <template slot-scope="{row}">
            <el-button type="primary" size="mini" @click="deleteViewData(row)">
              Confirm
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>

    <el-dialog :title="textMap[dialogViewIpStatus]" :visible.sync="dialogFormViewIpVisible">
      <div class="filter-container" :model="viewip_temp">
        <el-input v-model="viewip_temp.ip" placeholder="vip" style="width: 200px;" class="filter-item" @keyup.enter.native="handleViewIpFilter" />
        <el-input v-model="viewip_temp.node" placeholder="node" style="width: 200px;" class="filter-item" @keyup.enter.native="handleViewIpFilter" />
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
    <pagination v-show="viewiptotal>0" :total="viewiptotal" :page.sync="viewippage" :limit.sync="viewiplimit" @pagination="getViewIpList" />
    </el-dialog>

    <el-dialog :title="textMap[dialogNameidViewIpUpdateStatus]" :visible.sync="dialogFormNameidViewIpUpdateVisible">
      <el-form ref="dataViewIpForm" :model="viewip_update_temp" label-position="left" label-width="200px" style="width: 400px; margin-left:50px;">
        <el-form-item label="vipaddress" prop="record">
          <el-input v-model="viewip_update_temp.nameid_device_id.vip_address" />
        </el-form-item>
        <el-form-item label="ratio" prop="record">
          <el-input v-model="viewip_update_temp.nameid_device_ratio" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormNameidViewIpUpdateVisible = false">
          Cancel
        </el-button>
        <el-button type="primary" @click="updateViewIpData()">
          Confirm
        </el-button>
      </div>
    </el-dialog>

    <el-dialog :title="textMap[dialogNameidViewIpDeleteStatus]" :visible.sync="dialogFormNameidViewIpDeleteVisible">
      <el-table
        ref="viewtable"
        :key="tableKey"
        v-loading="deleteviewipLoading"
        :data="deleteviewipdata"
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
        <el-table-column label="vip" sortable="custom" align="center" width="80">
          <template slot-scope="scope">
            <span>{{ scope.row.nameid_device_id.vip_address }}</span>
          </template>
        </el-table-column>
        <el-table-column label="ratio" width="350px" align="center">
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
            <el-button type="primary" size="mini" @click="deleteViewIpData(row)">
              Confirm
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>

    <el-dialog :title="textMap[dialogNameidViewIpStatus]" :visible.sync="dialogFormNameidViewIpVisible">
      <div class="filter-container" :model="ip_temp">
        <el-input v-model="ip_temp.country" placeholder="country" style="width: 200px;" class="filter-item" @keyup.enter.native="handleIpFilter" />
        <el-input v-model="ip_temp.isp" placeholder="isp" style="width: 200px;" class="filter-item" @keyup.enter.native="handleIpFilter" />
        <el-input v-model="ip_temp.region" placeholder="region" style="width: 200px;" class="filter-item" @keyup.enter.native="handleIpFilter" />
        <el-input v-model="ip_temp.province" placeholder="province" style="width: 200px;" class="filter-item" @keyup.enter.native="handleIpFilter" />
        <el-input v-model="ip_temp.city" placeholder="city" style="width: 200px;" class="filter-item" @keyup.enter.native="handleIpFilter" />
        <el-input v-model="ip_temp.nodeid" placeholder="nodeid" style="width: 200px;" class="filter-item" @keyup.enter.native="handleIpFilter" />
        <el-input v-model="ip_temp.ip" placeholder="ip" style="width: 200px;" class="filter-item" @keyup.enter.native="handleIpFilter" />
        <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleIpFilter">
          Search
        </el-button>
        <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFatherView">
          Fatherview
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
        <el-button @click="dialogFormNameidViewIpVisible = false">
          Cancel
        </el-button>
        <el-button type="primary" @click="createIpData()">
          Confirm
        </el-button>
      </div>
      <pagination v-show="iptotal>0" :total="iptotal" :page.sync="ippage" :limit.sync="iplimit" @pagination="handleViewIpCreate" />
    </el-dialog>

    <el-dialog :title="textMap[dialogNameidViewCnameStatus]" :visible.sync="dialogFormNameidViewCnameVisible">
      <div class="filter-container" :model="cname_temp">
        <el-input v-model="cname_temp.nameid_cname" placeholder="nameid_cname" style="width: 200px;" class="filter-item" @keyup.enter.native="handleCnameFilter" />
        <el-input v-model="cname_temp.nameid_owner" placeholder="nameid_owner" style="width: 200px;" class="filter-item" @keyup.enter.native="handleCnameFilter" />
        <el-input v-model="cname_temp.nameid_supplier" placeholder="nameid_supplier" style="width: 200px;" class="filter-item" @keyup.enter.native="handleCnameFilter" />
        <el-input v-model="cname_temp.nameid_business" placeholder="nameid_business" style="width: 200px;" class="filter-item" @keyup.enter.native="handleCnameFilter" />
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
        <el-button @click="dialogFormNameidViewCnameVisible = false">
          Cancel
        </el-button>
        <el-button type="primary" @click="createCnameData()">
          Confirm
        </el-button>
      </div>
      <pagination v-show="cnametotal>0" :total="cnametotal" :page.sync="cnamepage" :limit.sync="cnamelimit" @pagination="handleViewCnameCreate" />
    </el-dialog>

    <el-dialog :title="textMap[dialogViewCnameStatus]" :visible.sync="dialogFormViewCnameVisible">
      <div class="filter-container" :model="viewcname_temp">
        <el-input v-model="viewcname_temp.cname" placeholder="cname" style="width: 200px;" class="filter-item" @keyup.enter.native="handleViewCnameFilter" />
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
      <pagination v-show="viewcnametotal>0" :total="viewcnametotal" :page.sync="viewcnamepage" :limit.sync="viewcnamelimit" @pagination="getViewCnameList" />
    </el-dialog>
    <el-dialog :title="textMap[this.dialogNameidViewCnameUpdateStatus]" :visible.sync="this.dialogFormNameidViewCnameUpdateVisible">
      <el-form ref="dataViewCnameForm" :model="cnameratio_temp" label-position="left" label-width="200px" style="width: 400px; margin-left:50px;">
        <el-form-item label="cname" prop="record">
          <el-input v-model="cnameratio_temp.nameid_cname_id.nameid_cname" />
        </el-form-item>
        <el-form-item label="ratio" prop="record">
          <el-input v-model="cnameratio_temp.nameid_cname_ratio" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormNameidViewCnameUpdateVisible = false">
          Cancel
        </el-button>
        <el-button type="primary" @click="updateViewCnameData()">
          Confirm
        </el-button>
      </div>
    </el-dialog>

    <el-dialog :title="textMap[dialogNameidViewCnameDeleteStatus]" :visible.sync="dialogFormNameidViewCnameDeleteVisible">
      <el-table
        ref="viewtable"
        :key="tableKey"
        v-loading="deleteviewcnameLoading"
        :data="deleteviewcnamedata"
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
            <el-button type="primary" size="mini" @click="deleteViewCnameData(row)">
              Confirm
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>
    <el-dialog :title="textMap[dialogCopyStatus]" :visible.sync="dialogFormCopyVisible">
      <el-form ref="dataCopyForm" :model="copy_temp" label-position="left" label-width="120px" style="width: 400px; margin-left:50px;">
        <el-form-item label="nameid_name" prop="record">
          <el-input v-model="copy_temp.nameid_name" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">
          Cancel
        </el-button>
        <el-button type="primary" @click="GenerateCopyName">
          Confirm
        </el-button>
      </div>
    </el-dialog>

    <el-dialog :title="textMap[dialogViewFatherStatus]" :visible.sync="dialogFormFatherVisible">
    <el-table
      ref="viewtable"
      :key="tableKeys"
      v-loading="fatherviewlistLoading"
      :data="fatherviewlist"
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
      <el-table-column label="view_default">
        <template slot-scope="scope">
          <span>{{ scope.row.view_default }}</span>
        </template>
      </el-table-column>
      <el-table-column label="view_country">
        <template slot-scope="scope">
          <span>{{ scope.row.view_country }}</span>
        </template>
      </el-table-column>
      <el-table-column label="view_isp">
        <template slot-scope="scope">
          <span>{{ scope.row.view_isp }}</span>
        </template>
      </el-table-column>
      <el-table-column label="view_region">
        <template slot-scope="scope">
          <span>{{ scope.row.view_region }}</span>
        </template>
      </el-table-column>
      <el-table-column label="view_province">
        <template slot-scope="scope">
          <span>{{ scope.row.view_province }}</span>
        </template>
      </el-table-column>
      <el-table-column label="view_city">
        <template slot-scope="scope">
          <span>{{ scope.row.view_city }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Actions" align="center" width="300px" class-name="small-padding fixed-width">
        <template slot-scope="{row}">
          <el-button type="primary" size="mini" @click="handleFatheridAdd(row)">
            add
          </el-button>
          <el-button v-if="row.status!='deleted'" size="mini" type="danger" @click="handleFatheridCancel(row)">
            cancel
          </el-button>
        </template>
      </el-table-column>
     </el-table>
     <div slot="footer" class="dialog-footer">
       <el-button @click="dialogFormFatherVisible = false">
         Cancel
       </el-button>
       <el-button type="primary" @click="dialogFormFatherVisible = false">
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
import { copyname, generateView, fetchFatherview, fetchIpList, fetchViewIpList, fetchCnameList, fetchViewCnameList, fetchSpecialView, fetchView, generateConfig, fetchDnstype, fetchZone, fetchNameidpolicy, deleteid, fetchList, create, update, createview, updateview, updateviewip, updateviewcname, deleteviewid, deleteviewipid, deleteviewcnameid, createviewip, createviewcname } from '@/api/analytical'
import waves from '@/directive/waves' // waves directive
import Pagination from '@/components/Pagination' // secondary package based on el-pagination
import VDistpicker from '@/v-distpicker'
// import VDistpicker from 'v-distpicker'
import './directives.js'
const status_swicth = ['enable', 'disable']
const nameid_status_swicth = ['disable']
const resolve_type_choice = ['cname', 'a', 'aaaa']
const preferred_type_choice = ['ratio', 'rr']
// arr to obj, such as { CN : "China", US : "USA" }

export default {
  name: 'ComplexTable',
  components: { Pagination, VDistpicker },
  directives: { waves },
  data() {
    return {
      row: '',
      tableKey: 0,
      tableKeys: 0,
      list: null,
      deletedata: null,
      listLoading: true,
      deleteLoading: true,
      search_temp: {
        nameid: ''
      },
      total: 0,
      page: 1,
      limit: 10,
      temp: {
        nameid_name: '',
        zone_type: '',
        dns_type: '',
        nameid_status: '',
        nameid_policy: ''
      },
      dialogFormVisible: false,
      dialogDeleteFormVisible: false,
      dialogStatus: '',
      dialogDeleteStatus: '',

      nameid_idx: -1,
      nameidviewid_idx: -1,
      nameidviewidadd_idx: -1,
      viewlist: null,
      deleteviewdata: null,
      viewlistLoading: true,
      deleteviewLoading: true,
      viewtotal: 0,
      viewpage: 1,
      viewlimit: 10,
      view_temp: {
        nameid_id: '',
        nameid_view_id: '',
        nameid_resolve_type: '',
        nameid_max_ip: '',
        nameid_preferred: '',
        nameid_status: '',
        nameid_ttl: ''
      },
      // 展示view
      dialogFormViewVisible: false,
      dialogViewStatus: '',
      // 删除view
      dialogDeleteFormViewVisible: false,
      dialogDeleteViewStatus: '',
      // 新增view的
      dialogFormNameidViewVisible: false,
      dialogNameidViewStatus: '',
      // 更新view的
      dialogFormNameidViewUpdateVisible: false,
      dialogNameidViewUpdateStatus: '',

      // viewip相关的
      // 记录弹窗对应的nameid和viewid
      nameid_ip_idx: -1,
      nameidviewid_ip_idx: -1,
      nameidviewid_iplist_idx: [],
      viewiplist: null,
      viewiplistLoading: true,
      deleteviewipdata: null,
      deleteviewipLoading: true,
      viewiptotal: 0,
      viewippage: 1,
      viewiplimit: 10,
      viewip_temp: {
        ip: '',
        node: ''
      },
      // 展示viewip
      dialogFormViewIpVisible: false,
      dialogViewIpStatus: '',

      // 给每一个view新增ip,这里展示ip信息
      iplist: null,
      iplistLoading: true,
      iptotal: 0,
      ippage: 1,
      iplimit: 10,
      iplist_temp: [],
      ip_temp: {
        country: '',
        isp: '',
        region: '',
        province: '',
        city: '',
        ip: '',
        node: ''
      },
      // 修改设备ration的时候
      viewip_update_temp: {
        nameid_device_id: '',
        nameid_device_ratio: ''
      },
      // 展示所有的ip资源信息
      dialogNameidViewIpStatus: '',
      dialogFormNameidViewIpVisible: false,

      // 修改viewip信息
      dialogNameidViewIpUpdateStatus: '',
      dialogFormNameidViewIpUpdateVisible: false,
      // 删除viewip信息
      dialogNameidViewIpDeleteStatus: '',
      dialogFormNameidViewIpDeleteVisible: false,

      // viewcname相关的
      // 记录弹窗对应的nameid和viewid
      nameid_cname_idx: -1,
      nameidviewid_cname_idx: -1,
      viewcnamelist: null,
      viewcnamelistLoading: true,
      deleteviewcnamedata: null,
      deleteviewcnameLoading: true,
      viewcnametotal: 0,
      viewcnamepage: 1,
      viewcnamelimit: 10,
      viewcname_temp: {
        cname: ''
      },
      // 展示viewcname
      dialogFormViewCnameVisible: false,
      dialogViewCnameStatus: '',
      // 给每一个view新增cname
      cnamelist: null,
      cnamelistLoading: true,
      cnametotal: 0,
      cnamepage: 1,
      cnamelimit: 10,
      cnamelist_temp: [],
      // 用于筛选cname的
      cname_temp: {
        nameid_cname: '',
        nameid_owner: '',
        nameid_supplier: '',
        nameid_business: ''
      },
      // 展示所有的cname资源信息
      dialogNameidViewCnameStatus: '',
      dialogFormNameidViewCnameVisible: false,
      // 修改cname ratio
      cnameratio_temp: {
        nameid_cname_id: '',
        nameid_cname_ratio: ''
      },
      // 修改viewcname信息
      dialogNameidViewCnameUpdateStatus: '',
      dialogFormNameidViewCnameUpdateVisible: false,
      // 删除viewcname信息
      dialogNameidViewCnameDeleteStatus: '',
      dialogFormNameidViewCnameDeleteVisible: false,

      // 生成配置文件用到的
      nameid_id_idx: -1,
      view_id_idx: -1,
      // 拷贝域名
      dialogFormCopyVisible: false,
      dialogCopyStatus: '',
      copy_temp: {
        nameid_name: ''
      },

      // 展示父级view的
      fatherviewlist: null,
      fatherviewtotal: 0,
      fatherviewlistLoading: true,
      dialogFormFatherVisible: false,
      dialogViewFatherStatus: '',

      zonenamelist: '',
      dnstypelist: '',
      policylist: '',
      status_swicth,
      nameid_status_swicth,
      resolve_type_choice,
      preferred_type_choice,
      textMap: {
        update: 'Edit',
        create: 'Create',
        delete: 'Delete',
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
    onSelected(data) {
      debugger
      console.log(data)
      console.log(data.id)
      this.select.province = data.province
    },
    getList() {
      this.listLoading = true
      fetchList({ 'nameid': this.search_temp.nameid, 'page': this.page, 'size': this.limit }).then(response => {
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
    // 获取指定nameid下的所有的view信息
    handleConfig(nameid) {
      this.viewlistLoading = true
      this.dialogViewStatus = 'configview'
      this.nameid_idx = nameid
      fetchView({ 'nameid': this.nameid_idx, 'page': this.viewpage, 'size': this.viewlimit }).then(response => {
        this.dialogFormViewVisible = true
        this.viewlist = response.msg.results
        this.viewtotal = response.msg.count

        // Just to simulate the time of the request
        setTimeout(() => {
          this.viewlistLoading = false
        }, 1.5 * 1000)
      })
    },
    // 获取指定nameid和view下的view信息
    getSpecialViewList(data) {
      this.nameidviewid_idx = data
      fetchSpecialView({ 'nameid': this.nameid_idx, 'viewid': this.nameidviewid_idx, 'page': this.viewpage, 'size': this.viewlimit }).then(response => {
        this.viewlist = response.msg.results
        this.viewtotal = response.msg.count

        // Just to simulate the time of the request
        setTimeout(() => {
          this.viewlistLoading = false
        }, 1.5 * 1000)
      })
    },
    // 在指定域名下创建新的view
    handleViewCreate() {
      this.resetViewTemp()
      this.dialogNameidViewStatus = 'create'
      this.dialogFormNameidViewVisible = true
      this.$nextTick(() => {
        this.$refs['dataViewForm'].clearValidate()
      })
    },
    // 选择要创建的viewid
    getNameidViewid(data) {
      this.nameidviewidadd_idx = data
    },
    createViewData() {
      this.view_temp.nameid_id = this.nameid_idx
      this.view_temp.nameid_view_id = this.nameidviewidadd_idx
      this.$refs['dataViewForm'].validate((valid) => {
        if (valid) {
          createview(this.view_temp).then(() => {
            this.viewlist.push(this.view_temp)
            this.dialogFormNameidViewVisible = false
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
    handleViewUpdate(row) {
      this.view_temp = Object.assign({}, row) // copy obj
      this.dialogFormNameidViewUpdateVisible = true
      this.dialogNameidViewUpdateStatus = 'update'
      this.$nextTick(() => {
        this.$refs['dataViewUpdateForm'].clearValidate()
      })
    },
    updateViewData() {
      this.$refs['dataViewUpdateForm'].validate((valid) => {
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
          updateview(tempData, id).then(() => {
            for (const v of this.viewlist) {
              if (v.id === this.view_temp.id) {
                const index = this.viewlist.indexOf(v)
                this.viewlist.splice(index, 1, this.view_temp)
                break
              }
            }
            this.dialogFormNameidViewUpdateVisible = false
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
    handleViewDelete(row) {
      var arr = []
      var tmp = {}
      for (var i in row) {
        tmp[i] = row[i]
      }
      arr.push(tmp)
      this.dialogDeleteViewStatus = 'delete'
      this.deleteviewLoading = true
      this.deleteviewdata = arr
      this.dialogDeleteFormViewVisible = true
      setTimeout(() => {
        this.deleteviewLoading = false
      }, 1.5 * 1000)
    },
    deleteViewData(row) {
      deleteviewid({ 'nameid': row.nameid_id.id, 'viewid': row.nameid_view_id.id }).then(() => {
        for (var v of this.viewlist) {
          if (v.id === row.id) {
            const index = this.viewlist.indexOf(v)
            this.viewlist.splice(index, 1)
            break
          }
        }
        this.dialogDeleteFormViewVisible = false
        this.$notify({
          title: 'Success',
          message: 'delete Successfully',
          type: 'success',
          duration: 2000
        })
      })
      this.dialogDeleteFormViewVisible = false
    },
    // 由前一个弹窗把nameid和viewid的信息带到新的弹窗
    handleViewIpConfig(row) {
      this.viewiplistLoading = true
      this.dialogViewIpStatus = 'configviewip'
      this.nameid_ip_idx = row.nameid_id.id
      this.nameidviewid_ip_idx = row.nameid_view_id.id
      this.nameidviewid_iplist_idx.push(row.nameid_view_id.id)
      fetchViewIpList({ 'nameid': this.nameid_ip_idx, 'viewid': this.nameidviewid_ip_idx, 'nodeid': this.viewip_temp.node, 'ip': this.viewip_temp.ip, 'page': this.viewippage, 'size': this.viewiplimit }).then(response => {
        this.dialogFormViewIpVisible = true
        this.viewiplist = response.msg.results
        this.viewiptotal = response.msg.count

        // Just to simulate the time of the request
        setTimeout(() => {
          this.viewiplistLoading = false
        }, 1.5 * 1000)
      })
    },
    // 单纯的指定nameid viewid和设备信息进行过滤
    handleViewIpFilter() {
      this.viewippage = 1
      this.getViewIpList()
    },
    getViewIpList() {
      this.viewiplistLoading = true
      fetchViewIpList({ 'nameid': this.nameid_ip_idx, 'viewid': this.nameidviewid_ip_idx, 'nodeid': this.viewip_temp.node, 'ip': this.viewip_temp.ip, 'page': this.viewippage, 'size': this.viewiplimit }).then(response => {
        this.viewiplist = response.msg.results
        this.viewiptotal = response.msg.count

        // Just to simulate the time of the request
        setTimeout(() => {
          this.viewiplistLoading = false
        }, 1.5 * 1000)
      })
    },
    // 修改每个ip的ratio
    handleViewIpUpdate(row) {
      this.viewip_update_temp = Object.assign({}, row) // copy obj
      this.dialogFormNameidViewIpUpdateVisible = true
      this.dialogNameidViewIpUpdateStatus = 'update'
      this.$nextTick(() => {
        this.$refs['dataViewIpForm'].clearValidate()
      })
    },
    updateViewIpData() {
      this.$refs['dataViewIpForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.viewip_update_temp)
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
          updateviewip(tempData, id).then(() => {
            for (const v of this.viewiplist) {
              if (v.id === this.viewip_update_temp.id) {
                const index = this.viewiplist.indexOf(v)
                this.viewiplist.splice(index, 1, this.viewip_update_temp)
                break
              }
            }
            this.dialogFormNameidViewIpUpdateVisible = false
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
    // 处理每个父级的location是否添加该ip
    handleFatherView() {
      this.fatherviewlistLoading = true
      this.dialogViewFatherStatus = 'create'
      fetchFatherview({ 'viewid': this.nameidviewid_ip_idx }).then(response => {
        this.dialogFormFatherVisible = true
        this.fatherviewlist = response.msg

        // Just to simulate the time of the request
        setTimeout(() => {
          this.fatherviewlistLoading = false
        }, 1.5 * 1000)
      })
    },
    handleFatheridAdd(row) {
      this.nameidviewid_iplist_idx.push(row.id)
      this.$notify({
        title: 'Success',
        message: 'Add Successfully',
        type: 'success',
        duration: 2000
      })
    },
    handleFatheridCancel(row) {
      var index = this.nameidviewid_iplist_idx.indexOf(row.id)
      if (index !== -1) {
        this.nameidviewid_iplist_idx.splice(index, 1)
      }
      this.$notify({
        title: 'Success',
        message: 'Cancel Successfully',
        type: 'success',
        duration: 2000
      })
    },
    // 给每个view新增ip的时候,需要对ip进行筛选
    handleIpFilter() {
      this.ippage = 1
      this.handleViewIpCreate()
    },
    handleViewIpCreate() {
      this.resetViewIpTemp()
      this.dialogNameidViewIpStatus = 'create'
      this.iplistLoading = true
      fetchIpList({ 'country': this.ip_temp.country, 'isp': this.ip_temp.isp, 'region': this.ip_temp.region, 'province': this.ip_temp.province, 'city': this.ip_temp.city, 'nodeid': this.ip_temp.nodeid, 'ip': this.ip_temp.ip, 'page': this.ippage, 'size': this.iplimit }).then(response => {
        this.dialogFormNameidViewIpVisible = true
        this.iplist = response.msg.results
        this.iptotal = response.msg.count

        // Just to simulate the time of the request
        setTimeout(() => {
          this.iplistLoading = false
        }, 1.5 * 1000)
      })
    },
    // 选中ip添加
    handleIpAdd(row) {
      this.iplist_temp.push(row.id)
      this.$notify({
        title: 'Success',
        message: 'Add Successfully',
        type: 'success',
        duration: 2000
      })
    },
    // 剔除本次选中的ip
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
    // 选好ip以后给每个view新增ip
    createIpData() {
      createviewip({ 'nameid': this.nameid_ip_idx, 'viewidinfo': this.nameidviewid_iplist_idx, 'devidinfo': this.iplist_temp }).then(() => {
        this.dialogFormNameidViewIpVisible = false
        this.$notify({
          title: 'Success',
          message: 'Created Successfully',
          type: 'success',
          duration: 2000
        })
      })
      this.iplist_temp = []
    },
    handleViewIpDelete(row) {
      var arr = []
      var tmp = {}
      for (var i in row) {
        tmp[i] = row[i]
      }
      arr.push(tmp)
      this.dialogNameidViewIpDeleteStatus = 'delete'
      this.deleteviewipLoading = true
      this.deleteviewipdata = arr
      this.dialogFormNameidViewIpDeleteVisible = true
      setTimeout(() => {
        this.deleteviewipLoading = false
      }, 1.5 * 1000)
    },
    deleteViewIpData(row) {
      var id = row.id
      deleteviewipid(id).then(() => {
        for (var v of this.viewiplist) {
          if (v.id === row.id) {
            const index = this.viewiplist.indexOf(v)
            this.viewiplist.splice(index, 1)
            break
          }
        }
        this.dialogFormNameidViewIpDeleteVisible = false
        this.$notify({
          title: 'Success',
          message: 'delete Successfully',
          type: 'success',
          duration: 2000
        })
      })
    },
    // 开始cname的配置
    handleViewCnameConfig(row) {
      this.viewcnamelistLoading = true
      this.dialogViewCnameStatus = 'configviewcname'
      this.nameid_cname_idx = row.nameid_id.id
      this.nameidviewid_cname_idx = row.nameid_view_id.id
      fetchViewCnameList({ 'nameid': this.nameid_cname_idx, 'viewid': this.nameidviewid_cname_idx, 'cname': this.viewcname_temp.cname, 'page': this.viewcnamepage, 'size': this.viewcnamelimit }).then(response => {
        this.dialogFormViewCnameVisible = true
        this.viewcnamelist = response.msg.results
        this.viewcnametotal = response.msg.count

        // Just to simulate the time of the request
        setTimeout(() => {
          this.viewcnamelistLoading = false
        }, 1.5 * 1000)
      })
    },
    // 过滤指定view的cname
    handleViewCnameFilter() {
      this.cnamepage = 1
      this.getViewCnameList()
    },
    getViewCnameList() {
      this.viewcnamelistLoading = true
      fetchViewCnameList({ 'nameid': this.nameid_cname_idx, 'viewid': this.nameidviewid_cname_idx, 'cname': this.viewcname_temp.cname, 'page': this.viewcnamepage, 'size': this.viewcnamelimit }).then(response => {
        this.viewcnamelist = response.msg.results
        this.viewcnametotal = response.msg.count

        // Just to simulate the time of the request
        setTimeout(() => {
          this.viewcnamelistLoading = false
        }, 1.5 * 1000)
      })
    },
    // 添加cname的时候，给指定view显示所有可用的cname,且支持过滤
    handleCnameFilter() {
      this.cnamepage = 1
      this.handleViewCnameCreate()
    },
    handleViewCnameCreate() {
      this.resetViewCnameTemp()
      this.dialogNameidViewCnameStatus = 'create'
      this.cnamelistLoading = true
      fetchCnameList({ 'cname': this.cname_temp.nameid_cname, 'operator': this.cname_temp.nameid_owner, 'supplier': this.cname_temp.nameid_supplier, 'business': this.cname_temp.nameid_business, 'page': this.cnamepage, 'size': this.cnamelimit }).then(response => {
        this.dialogFormNameidViewCnameVisible = true
        this.cnamelist = response.msg.results
        this.cnametotal = response.msg.count

        // Just to simulate the time of the request
        setTimeout(() => {
          this.cnamelistLoading = false
        }, 1.5 * 1000)
      })
    },
    // 选择上面的cname进行添加
    handleCnameAdd(row) {
      this.cnamelist_temp.push(row.id)
      this.$notify({
        title: 'Success',
        message: 'Add Successfully',
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
    // 选好cname以后进行创建
    createCnameData() {
      createviewcname({ 'nameid': this.nameid_cname_idx, 'viewidinfo': [this.nameidviewid_cname_idx], 'cnameinfo': this.cnamelist_temp }).then(() => {
        this.dialogFormNameidViewCnameVisible = false
        this.$notify({
          title: 'Success',
          message: 'Created Successfully',
          type: 'success',
          duration: 2000
        })
      })
      this.cnamelist_temp = []
    },
    // 修改每个cname的ratio
    handleViewCnameUpdate(row) {
      this.cnameratio_temp = Object.assign({}, row) // copy obj
      this.dialogFormNameidViewCnameUpdateVisible = true
      this.dialogNameidViewCnameUpdateStatus = 'update'
      this.$nextTick(() => {
        this.$refs['dataViewCnameForm'].clearValidate()
      })
    },
    getZonename() {
      fetchZone().then(response => {
        this.zonenamelist = response.msg
      })
    },
    getDnstype() {
      fetchDnstype().then(response => {
        this.dnstypelist = response.msg
      })
    },
    getNameidpolicy() {
      fetchNameidpolicy().then(response => {
        this.policylist = response.msg
      })
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
    resetTemp() {
      this.temp = {
        nameid_name: '',
        zone_type: '',
        dns_type: '',
        nameid_status: '',
        nameid_policy: ''
      }
    },
    resetViewTemp() {
      this.view_temp = {
        nameid_id: '',
        nameid_view_id: '',
        nameid_resolve_type: '',
        nameid_max_ip: '',
        nameid_preferred: '',
        nameid_status: '',
        nameid_ttl: ''
      }
    },
    resetViewIpTemp() {
      this.view_temp = {
        nameid_id: '',
        nameid_view_id: '',
        nameid_resolve_type: '',
        nameid_max_ip: '',
        nameid_preferred: '',
        nameid_status: '',
        nameid_ttl: ''
      }
    },
    resetViewCnameTemp() {
      this.view_temp = {
        nameid_id: '',
        nameid_view_id: '',
        nameid_resolve_type: '',
        nameid_max_ip: '',
        nameid_preferred: '',
        nameid_status: '',
        nameid_ttl: ''
      }
    },
    updateViewCnameData() {
      this.$refs['dataViewCnameForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.cnameratio_temp)
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
          updateviewcname(tempData, id).then(() => {
            for (const v of this.viewcnamelist) {
              if (v.id === this.cnameratio_temp.id) {
                const index = this.viewcnamelist.indexOf(v)
                this.viewcnamelist.splice(index, 1, this.cnameratio_temp)
                break
              }
            }
            this.dialogFormNameidViewCnameUpdateVisible = false
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
    handleViewCnameDelete(row) {
      var arr = []
      var tmp = {}
      for (var i in row) {
        tmp[i] = row[i]
      }
      arr.push(tmp)
      this.dialogNameidViewCnameDeleteStatus = 'delete'
      this.deleteviewcnameLoading = true
      this.deleteviewcnamedata = arr
      this.dialogFormNameidViewCnameDeleteVisible = true
      setTimeout(() => {
        this.deleteviewcnameLoading = false
      }, 1.5 * 1000)
    },
    deleteViewCnameData(row) {
      var id = row.id
      deleteviewcnameid(id).then(() => {
        for (var v of this.viewcnamelist) {
          if (v.id === row.id) {
            const index = this.viewcnamelist.indexOf(v)
            this.viewcnamelist.splice(index, 1)
            break
          }
        }
        this.dialogFormNameidViewCnameDeleteVisible = false
        this.$notify({
          title: 'Success',
          message: 'delete Successfully',
          type: 'success',
          duration: 2000
        })
      })
    },
    handleGenerate() {
      generateConfig({ 'nameid': this.search_temp.nameid }).then(response => {
        this.$notify({
          title: 'Success',
          message: 'generate Successfully',
          type: 'success',
          duration: 2000
        })
      })
    },
    GenerateView(row) {
      this.nameid_id_idx = row.nameid_id.id
      this.view_id_idx = row.nameid_view_id.id
      generateView({ 'nameid': this.nameid_id_idx, 'viewid': this.view_id_idx }).then(response => {
        // Just to simulate the time of the request
        this.$notify({
          title: 'Success',
          message: 'generate Successfully',
          type: 'success',
          duration: 2000
        })
      })
    },
    handleCopyName() {
      this.copy_temp = {
        nameid_name: ''
      }
      this.dialogCopyStatus = 'create'
      this.dialogFormCopyVisible = true
      this.$nextTick(() => {
        this.$refs['dataCopyForm'].clearValidate()
      })
    },
    GenerateCopyName() {
      this.$refs['dataCopyForm'].validate((valid) => {
        if (valid) {
          copyname({ 'nameid': this.copy_temp.nameid_name, 'oldnameid': this.search_temp.nameid }).then(response => {
            this.dialogFormCopyVisible = false
            this.$notify({
              title: 'Success',
              message: 'Created Successfully',
              type: 'success',
              duration: 2000
            })
          })
        }
      })
    }
  }
}
</script>
