webpackJsonp([32],{EW6a:function(e,t){},P4Q3:function(e,t,a){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var n=a("zL8q"),i={name:"banner",data:function(){return{loading:!1,search:"",treeData:[],multipleSelection:[],tableData:[],total:"0"}},created:function(){this.getData()},methods:{getWinHeight:a("F+jZ").d,handleSelectionChange:function(e){this.multipleSelection=e.map(function(e){return e.ibid})},handleEdit:function(e){this.$router.push("banner/bannerOperate/"+e)},handleDelete:function(e){var t=this,a={ibid:e};Object(n.MessageBox)({title:"提示",message:"此操作将永久删除数据, 是否继续？",showCancelButton:!0,confirmButtonText:"确定",cancelButtonText:"取消",beforeClose:function(e,i,l){"confirm"===e?(i.confirmButtonLoading=!0,i.confirmButtonText="执行中...",t.$http({method:"POST",url:"/index/delete_banner_show/",data:a,params:{token:t.Cookie.get("token")}}).then(function(e){i.confirmButtonLoading=!1,200==e.status?(Object(n.Message)({type:"success",message:e.message,duration:1e3}),t.getData()):Object(n.Message)({type:"error",message:e.message,duration:1e3}),i.confirmButtonLoading=!1,l()})):l()}})},getData:function(){var e=this;this.loading=!0,this.$http({method:"get",url:"/index/banner/"}).then(function(t){200==t.status?t.data?e.tableData=t.data:e.tableData=null:(e.tableData=null,Object(n.Message)({type:"error",message:t.message,duration:2e3})),e.loading=!1}).catch(function(){e.loading=!1})}}},l={render:function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"banner-container"},[a("div",{staticClass:"announcement-header"},[a("div",{staticClass:"header-left"},[a("b",[e._v("管理")]),e._v(" "),a("span",[e._v("共 "+e._s(e.total)+" 条")])]),e._v(" "),a("div",{staticClass:"header-right"},[a("router-link",{attrs:{to:"banner/bannerOperate/0",title:"新增"}},[a("el-button",{attrs:{type:"primary",size:"mini",icon:"el-icon-plus"}})],1)],1)]),e._v(" "),a("div",{staticClass:"announcement-list",style:{height:e.getWinHeight()-315+"px"}},[a("el-table",{directives:[{name:"loading",rawName:"v-loading",value:e.loading,expression:"loading"}],ref:"multipleTable",staticStyle:{width:"100%"},attrs:{data:e.tableData,"tooltip-effect":"dark",border:"",stripe:""},on:{"selection-change":e.handleSelectionChange}},[a("el-table-column",{attrs:{prop:"ibimage",label:"图片",align:"center","show-overflow-tooltip":""},scopedSlots:e._u([{key:"default",fn:function(e){return[a("img",{staticClass:"product-img",attrs:{src:e.row.ibimage,alt:""}})]}}])}),e._v(" "),a("el-table-column",{attrs:{prop:"iblink",label:"链接",align:"center"}}),e._v(" "),a("el-table-column",{attrs:{prop:"ibsort",label:"排序号",align:"center"}}),e._v(" "),a("el-table-column",{attrs:{prop:"name",label:"操作",align:"center"},scopedSlots:e._u([{key:"default",fn:function(t){return[a("div",[a("el-button",{staticClass:"el-icon-delete",attrs:{size:"mini",type:"danger",title:"删除"},on:{click:function(a){e.handleDelete(t.row.ibid)}}})],1)]}}])})],1)],1)])},staticRenderFns:[]};var o=a("VU/8")(i,l,!1,function(e){a("EW6a")},null,null);t.default=o.exports}});