<template>
  <div :class="wrapper">
    <template v-if="type != 'mobile'">
      <select @change="getIsps" v-model="currentCountry" :disabled="disabled || countryDisabled">
        <option :value="placeholders.country">{{ placeholders.country }}</option>
        <option v-for="(item, index) in countrys"
                :value="item"
                :key="index">
          {{ item }}
        </option>
      </select>
      <select @change="getRegions" v-model="currentIsp" :disabled="disabled || ispDisabled">
        <option :value="placeholders.isp">{{ placeholders.isp }}</option>
        <option v-for="(item, index) in isps"
                :value="item"
                :key="index">
          {{ item }}
        </option>
      </select>
      <select @change="getProvinces" v-model="currentRegion" :disabled="disabled || regionDisabled">
	<option :value="placeholders.region">{{ placeholders.region }}</option>
	<option v-for="(item, index) in regions"
		:value="item"
		:key="index">
	  {{ item }}
	</option>
      </select>
      <select @change="getCities" v-model="currentProvince" :disabled="disabled || provinceDisabled">
        <option :value="placeholders.province">{{ placeholders.province }}</option>
        <option v-for="(item, index) in provinces"
                :value="item"
                :key="index">
          {{ item }}
        </option>
      </select>
      <select @change="getAreas" v-model="currentCity" :disabled="disabled || cityDisabled">
        <option :value="placeholders.city">{{ placeholders.city }}</option>
        <option v-for="(item, index) in cities"
                :value="item"
                :key="index">
          {{ item }}
        </option>
      </select>
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        Confirm
      </el-button>
    </template>
    <template v-else>
      <div :class="addressHeader">
        <ul>
          <li :class="{'active': tab === 1}" @click="resetProvince">{{ currentProvince && !staticPlaceholder ? currentProvince : placeholders.province }}</li>
          <template v-if="!onlyProvince">
            <li v-if="showCityTab" :class="{'active': tab === 2}" @click="resetCity">{{  currentCity && !staticPlaceholder ? currentCity : placeholders.city }}</li>
            <li v-if="showAreaTab && !hideArea" :class="{'active': tab === 3}">{{ currentArea && !staticPlaceholder ? currentArea : placeholders.area }}</li>
          </template>
        </ul>
      </div>
      <div :class="addressContainer">
        <ul v-if="tab === 1">
          <li v-for="(item, index) in provinces"
              :class="{'active': item === currentProvince}"
              @click="chooseProvince(item)"
              :key="index">
            {{ item }}
          </li>
        </ul>
        <template v-if="!onlyProvince">
          <ul v-if="tab === 2">
            <li v-for="(item, index) in cities"
                :class="{'active': item === currentCity}"
                @click="chooseCity(item)"
                :key="index">
              {{ item }}
            </li>
          </ul>
          <ul v-if="tab === 3 && !hideArea">
            <li v-for="(item, index) in areas"
                :class="{'active': item === currentArea}"
                @click="chooseArea(item)"
                :key="index">
              {{ item }}
            </li>
          </ul>
        </template>
      </div>
    </template>
  </div>
</template>

<script>
import DISTRICTS from './districts';

// const DEFAULT_CODE = 100000;
const DEFAULT_CODE = 1;

export default {
  name: 'v-distpicker',
  props: {
    province: { type: [String, Number], default: '' },
    city: { type: [String, Number], default: '' },
    area: { type: [String, Number], default: '' },
    type: { type: String, default: '' },
    hideArea: { type: Boolean, default: false },
    onlyProvince: { type: Boolean, default: false },
    staticPlaceholder: { type: Boolean, default: false },
    placeholders: {
      type: Object,
      default() {
        return {
          default: 'default',
          country: '国家',
          isp: '运营商',
          region: '大区',
          province: '省',
          city: '市',
          area: '区',
        }
      }
    },
    disabled: { type: Boolean, default: false },
    countryDisabled: { type: Boolean, default: false },
    ispDisabled: { type: Boolean, default: false },
    regionDisabled: { type: Boolean, default: false },
    provinceDisabled: { type: Boolean, default: false },
    cityDisabled: { type: Boolean, default: false },
    areaDisabled: { type: Boolean, default: false },
    addressHeader: { type: String, default: 'address-header' },
    addressContainer: { type: String, default: 'address-container' },
    wrapper: { type: String, default: 'distpicker-address-wrapper' },
  },
  data() {
    return {
      id: -1,
      tab: 1,
      showIspTab: false,
      showRegionTab: false,
      showProvinceTab: false,
      showCityTab: false,
      showAreaTab: false,
      default: [],
      countrys: [],
      isps: [],
      regions: [],
      provinces: [],
      cities: [],
      areas: [],
      currentCountry: this.determineType(this.country) || this.placeholders.country,
      currentIsp: this.determineType(this.isp) || this.placeholders.isp,
      currentRegion: this.determineType(this.region) || this.placeholders.region,
      currentProvince: this.determineType(this.province) || this.placeholders.province,
      currentCity: this.determineType(this.city) || this.placeholders.city,
      currentArea: this.determineType(this.area) || this.placeholders.area,
    }
  },
  created() {
    if (this.type != 'mobile') {
      // this.countrys = this.getCountry()
      // this.provinces = this.getDistricts()
      this.countrys = this.getDistricts()
      this.cities = this.province ? this.getDistricts(this.getAreaCode(this.determineType(this.province))) : []
      this.areas = this.city ? this.getDistricts(this.getAreaCode(this.determineType(this.city), this.area)) : []
    }
    /*
     else {
      if (this.area && !this.hideArea && !this.onlyProvince) {
        this.tab = 3
        this.showCityTab = true
        this.showAreaTab = true
        this.areas = this.getDistricts(this.getAreaCode(this.determineType(this.city), this.area))
      } else if (this.city && this.hideArea && !this.onlyProvince) {
        this.tab = 2
        this.showCityTab = true
        this.cities = this.getDistricts(this.getAreaCode(this.determineType(this.province)))
      } else {
        this.provinces = this.getDistricts()
      }
    }
    */
  },
  watch: {
    currentIsp(vaule) {
      this.$emit('isp', this.setData(vaule))
      if (this.onlyProvince) this.emit('selected')
    },
    currentRegion(vaule) {
      this.$emit('region', this.setData(vaule))
      if (this.onlyProvince) this.emit('selected')
    },
    currentProvince(vaule) {
      this.$emit('province', this.setData(vaule))
      if (this.onlyProvince) this.emit('selected')
    },
    currentCity(value) {
      this.$emit('city', this.setData(value, this.currentProvince))
      if (value != this.placeholders.city && this.hideArea) this.emit('selected')
    },
    currentArea(value) {
      this.$emit('area', this.setData(value, this.currentProvince))
      this.emit('selected')
    },
    isp(value) {
      this.currentIsp = this.isp || this.placeholders.isp
      this.regions = this.determineValue(this.currentIsp, this.placeholders.isp)
    },
    region(value) {
      this.currentRegion = this.region || this.placeholders.region
      this.provinces = this.determineValue(this.currentRegion, this.placeholders.region)
    },
    province(value) {
      this.currentProvince = this.province || this.placeholders.province
      this.cities = this.determineValue(this.currentProvince, this.placeholders.province)
    },
    city(value) {
      this.currentCity = this.city || this.placeholders.city
      this.areas = this.determineValue(this.currentCity, this.placeholders.city, this.currentProvince)
    },
    area(value) {
      this.currentArea = this.area || this.placeholders.area
    },
  },
  methods: {
    handleFilter() {
       debugger
       var fatherid = DEFAULT_CODE
       console.log(this.currentCity)
       console.log(fatherid)
       console.log(DEFAULT_CODE)
       if (this.currentCountry != '国家' ) {
         fatherid = this.getAreaCodeByPreCode(this.currentCountry,fatherid)
         console.log(fatherid)
       }
       if (this.currentIsp != '运营商' ) {
         fatherid = this.getAreaCodeByPreCode(this.currentIsp,fatherid)
         console.log(fatherid)
       }
       if (this.currentRegion != '大区' ) {
         fatherid = this.getAreaCodeByPreCode(this.currentRegion,fatherid)
         console.log(fatherid)
       }
       if (this.currentProvince != '省' ) {
         console.log(fatherid)
         console.log(this.currentProvince)
         fatherid = this.getAreaCodeByPreCode(this.currentProvince,fatherid)
         console.log(fatherid)
       }
       if (this.currentCity != '市' ) {
         fatherid = this.getAreaCodeByPreCode(this.currentCity,fatherid)
         console.log(fatherid)
       }
       console.log(this.currentCity)
       console.log(fatherid)
       this.id = fatherid
       this.$emit('getNameidViewList',fatherid);
       this.$emit('getid_add_fun',fatherid);
    },
    setData(value, check = '') {
      return {
        code: this.getAreaCode(value, check),
        value: value,
      }
    },
    emit(name) {
      let data = {
        province: this.setData(this.currentProvince)
      }

      if (!this.onlyProvince) {
        this.$set(data, 'city', this.setData(this.currentCity))
      }

      if (!this.onlyProvince || this.hideArea) {
        this.$set(data, 'area', this.setData(this.currentArea, this.currentCity))
      }

      this.$emit(name, data)
    },
    getCities() {
      this.currentCity = this.placeholders.city
      this.currentArea = this.placeholders.area
      this.cities = this.determineValue(this.currentProvince, this.placeholders.province)
      this.cleanList('areas')
      if (this.cities.length === 0) {
        this.emit('selected')
        this.tab = 4
        this.showCityTab = false
      }
    },
    getIsps() {
       this.currentIsp = this.placeholders.isp
       this.currentRegion = this.placeholders.region
       this.currentProvince = this.placeholders.province
       this.currentCity = this.placeholders.city
       this.currentArea = this.placeholders.area
       this.isps = this.determineValue(this.currentCountry, this.placeholders.country)
       this.cleanList('regions')
       if (this.isps.length === 0) {
        this.emit('selected')
        this.tab = 1
        this.showIspTab = false
       }
    },
    getRegions() {
       this.currentRegion = this.placeholders.region
       this.currentProvince = this.placeholders.province
       this.currentCity = this.placeholders.city
       this.currentArea = this.placeholders.area
       this.regions = this.determineValue(this.currentIsp, this.placeholders.isp)
       this.cleanList('provinces')
       if (this.regions.length === 0) {
        this.emit('selected')
        this.tab = 2
        this.showRegionTab = false
       }
    },
    getProvinces() {
       this.currentProvince = this.placeholders.province
       this.currentCity = this.placeholders.city
       this.currentArea = this.placeholders.area
       this.provinces = this.determineValue(this.currentRegion, this.placeholders.region)
       this.cleanList('citys')
       if (this.citys.length === 0) {
        this.emit('selected')
        this.tab = 3
        this.showProvinceTab = false
       }
    },
    
    getAreas() {
      this.currentArea = this.placeholders.area
      this.areas = this.determineValue(this.currentCity, this.placeholders.city, this.currentProvince)
      if (this.areas.length === 0) {
        this.emit('selected')
        this.tab = 5
        this.showAreaTab = false
      }
    },
    resetProvince() {
      this.tab = 1
      this.provinces = this.getDistricts()
      this.showCityTab = false
      this.showAreaTab = false
    },
    resetCity() {
      this.tab = 2
      this.showCityTab = true
      this.showAreaTab = false
      this.getCities()
    },
    chooseProvince(name) {
      this.currentProvince = name
      if (this.onlyProvince) return
      this.tab = 2
      this.showCityTab = true
      this.showAreaTab = false
      this.getCities()
    },
    chooseCity(name) {
      this.currentCity = name
      if (this.hideArea) return
      this.tab = 3
      this.showCityTab = true
      this.showAreaTab = true
      this.getAreas()
    },
    chooseArea(name) {
      this.currentArea = name
    },
    getAreaCodeByPreCode(name, preCode) {
      let codes = []

      for(let x in DISTRICTS) {
        for(let y in DISTRICTS[x]) {
          if(name === DISTRICTS[x][y]) {
            codes.push(y)
          }
        }
      }
      debugger
      console.log(codes)
      if (codes.length > 1) {
        let index
        codes.forEach((item, i) => {
          if (item.slice(0, 2) == preCode) {
            index = i
          }
        })

        return codes[index]
      } else {
        return codes[0]
      }
    },
    getAreaCode(name, check = '') {
      for(let x in DISTRICTS) {
        for(let y in DISTRICTS[x]) {
          if(name === DISTRICTS[x][y]) {
            if (check.length > 0) {
              if (y.slice(0, 2) !== this.getAreaCodeByPreCode(check, y.slice(0, 2)).slice(0, 2)) {
                continue
              } else {
                return y
              }
            } else {
              return y
            }
          }
        }
      }
    },
    getCodeValue(code) {
      for(let x in DISTRICTS) {
        for(let y in DISTRICTS[x]) {
          if(code === parseInt(y)) {
            return DISTRICTS[x][y]
          }
        }
      }
    },
    getDistricts(code = DEFAULT_CODE) {
      return DISTRICTS[code] || []
    },
    determineValue(currentValue, placeholderValue, check = '') {
      if(currentValue === placeholderValue) {
        return []
      } else {
        return this.getDistricts(this.getAreaCode(currentValue, check))
      }
    },
    determineType(value) {
      if(typeof value === 'number') {
        return this.getCodeValue(value)
      }

      return value
    },
    cleanList(name) {
      this[name] = []
    },
  }
}
</script>

<style lang="scss">
.distpicker-address-wrapper {
  color: #9caebf;
  select {
    padding: .5rem .75rem;
    height: 40px;
    font-size: 1rem;
    line-height: 1.25;
    color: #464a4c;
    background-color: #fff;
    background-image: none;
    -webkit-background-clip: padding-box;
    background-clip: padding-box;
    border: 1px solid rgba(0,0,0,.15);
    border-radius: .25rem;
    -webkit-transition: border-color ease-in-out .15s,-webkit-box-shadow ease-in-out .15s;
    transition: border-color ease-in-out .15s,-webkit-box-shadow ease-in-out .15s;
    -o-transition: border-color ease-in-out .15s,box-shadow ease-in-out .15s;
    transition: border-color ease-in-out .15s,box-shadow ease-in-out .15s;
    transition: border-color ease-in-out .15s,box-shadow ease-in-out .15s,-webkit-box-shadow ease-in-out .15s;

    option {
      font-weight: normal;
      display: block;
      white-space: pre;
      min-height: 1.2em;
      padding: 0px 2px 1px;
    }
  }
  ul {
    margin: 0;
    padding: 0;

    li {
      list-style: none;
    }
  }
  .address-header {
    background-color: #fff;

    ul {
      display: flex;
      justify-content: space-around;
      align-items: stretch;

      li {
        display: inline-block;
        padding: 10px 10px 7px;

        &.active {
          border-bottom: #52697f solid 3px;
          color: #52697f;
        }
      }
    }
  }
  .address-container {
    background-color: #fff;

    ul {
      height: 100%;
      overflow: auto;

      li {
        padding: 8px 10px;
        border-top: 1px solid #f6f6f6;

        &.active {
          color: #52697f;
        }
      }
    }
  }
}
.disabled-color{
    background: #f8f8f8;
}
</style>
