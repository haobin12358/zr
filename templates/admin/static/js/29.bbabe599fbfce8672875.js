webpackJsonp([29],{B9Yw:function(t,e,a){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var n,i=a("bOdI"),l=a.n(i),s=a("zL8q"),o=a("F+jZ"),c={name:"productMes",data:function(){return{enumOptions:[],loading:!1,search:"",multipleSelection:[],tableData:[],currentPage:1,total:0,pageSize:10}},created:function(){this.getData()},methods:(n={getWinHeight:o.d},l()(n,"getWinHeight",o.d),l()(n,"handleCurrentChange",function(t){this.currentPage=t,this.search?this.searchData(t):this.getData()}),l()(n,"formatter",function(t){return t.releasetime=t.releasetime.substr(0,10),t.releasetime}),l()(n,"handleSelectionChange",function(t){this.multipleSelection=t.map(function(t){return t.ID})}),l()(n,"handleEdit",function(t){this.$router.push("/clean/cleanOperate/"+t)}),l()(n,"handleDelete",function(t){var e=this,a={sceid:t};Object(s.MessageBox)({title:"提示",message:"此操作将永久删除数据, 是否继续？",showCancelButton:!0,confirmButtonText:"确定",cancelButtonText:"取消",beforeClose:function(t,n,i){"confirm"===t?(n.confirmButtonLoading=!0,n.confirmButtonText="执行中...",e.$http({method:"POST",url:"/cleaner/cancle_cleanselector/",data:a,params:{token:e.Cookie.get("token")}}).then(function(t){n.confirmButtonLoading=!1,200==t.status?(Object(s.Message)({type:"success",message:t.message,duration:1e3}),e.getData()):Object(s.Message)({type:"error",message:t.message,duration:1e3}),n.confirmButtonLoading=!1,i()})):i()}})}),l()(n,"getData",function(){var t=this;this.loading=!0,this.$http({method:"get",url:"/cleaner/clean_list_admin/",params:{token:this.Cookie.get("token"),page:this.currentPage,count:this.pageSize}}).then(function(e){200==e.status?e.data?(t.tableData=e.data.cleans,t.total=e.all_count):(t.tableData=null,t.total=e.all_count):(t.tableData=null,t.total=e.all_count,Object(s.Message)({type:"error",message:e.message,duration:2e3})),t.loading=!1}).catch(function(){t.loading=!1})}),l()(n,"searchData",function(){var t=this;this.loading=!0,this.$http({method:"get",url:"/MProduct/GetProductList",params:{token:this.Cookie.get("Ticket"),keyword:this.search,pageIndex:this.currentPage,pageSize:this.pageSize}}).then(function(e){e.status,t.tableData=e.data,t.total=e.all_count,t.loading=!1}).catch(function(){t.loading=!1})}),l()(n,"searchKeyword",function(){this.currentPage=1,this.handleCurrentChange(this.currentPage)}),n)},r={render:function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{staticClass:"clean-container"},[a("div",{staticClass:"announcement-header"},[a("div",{staticClass:"header-left"},[a("b",[t._v("管理")]),t._v(" "),a("span",[t._v("共 "+t._s(t.total)+" 条")])]),t._v(" "),a("div",{staticClass:"header-right"},[a("router-link",{attrs:{to:"/clean/cleanOperate/0",title:"新增"}},[a("el-button",{attrs:{type:"primary",size:"mini",icon:"el-icon-plus"}})],1)],1)]),t._v(" "),a("div",{staticClass:"announcement-list"},[a("el-table",{directives:[{name:"loading",rawName:"v-loading",value:t.loading,expression:"loading"}],ref:"multipleTable",staticStyle:{width:"100%"},attrs:{data:t.tableData,"tooltip-effect":"dark",border:"",stripe:""},on:{"selection-change":t.handleSelectionChange}},[a("el-table-column",{attrs:{prop:"scmtitlepic",label:"图标",align:"center"},scopedSlots:t._u([{key:"default",fn:function(e){return[null!=e.row.scmtitlepic?a("img",{staticClass:"product-img",attrs:{src:e.row.scmtitlepic}}):t._e()]}}])}),t._v(" "),a("el-table-column",{attrs:{prop:"scmtitle",label:"标题",align:"center","show-overflow-tooltip":""}}),t._v(" "),a("el-table-column",{attrs:{prop:"scmsubtitle",label:"简介",align:"center","show-overflow-tooltip":""}}),t._v(" "),a("el-table-column",{attrs:{prop:"scprice",label:"价格",align:"center"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("span",[t._v("￥"+t._s(e.row.scprice)+"/次")])]}}])}),t._v(" "),a("el-table-column",{attrs:{prop:"name",label:"操作",align:"center",width:"200px"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("div",[a("el-button",{staticClass:"el-icon-edit",attrs:{size:"mini",title:"编辑"},on:{click:function(a){t.handleEdit(e.row.sceid)}}}),t._v(" "),a("el-button",{staticClass:"el-icon-delete",attrs:{size:"mini",type:"danger",title:"删除"},on:{click:function(a){t.handleDelete(e.row.sceid)}}})],1)]}}])})],1)],1)])},staticRenderFns:[]};var u=a("VU/8")(c,r,!1,function(t){a("CpTN")},null,null);e.default=u.exports},CpTN:function(t,e){}});