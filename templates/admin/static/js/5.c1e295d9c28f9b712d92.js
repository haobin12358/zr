webpackJsonp([5],{Xdp4:function(e,t){},yHPh:function(e,t,a){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var n,l=a("bOdI"),o=a.n(l),s=a("zL8q"),i=a("F+jZ"),r={name:"productMes",data:function(){return{phone:"",gender:"",loading:!1,search:"",multipleSelection:[],tableData:[],currentPage:1,total:0,pageSize:10}},created:function(){this.getData()},methods:(n={getWinHeight:i.d},o()(n,"getWinHeight",i.d),o()(n,"filterTime",function(e){if(e)return e.slice(0,4)+"-"+e.slice(4,6)+"-"+e.slice(6,8)+" "+e.slice(8,10)+":"+e.slice(10,12)+":"+e.slice(12,14)}),o()(n,"setShowHome",function(e,t){var a=this,n="";n="",this.$http({method:"post",url:n,data:{adid:t},params:{token:this.Cookie.get("token")}}).then(function(e){200==e.status?(Object(s.Message)({message:e.message,type:"success",showClose:!0}),a.getData()):Object(s.Message)({message:e.message,type:"error",showClose:!0})})}),o()(n,"select",function(){this.currentPage=1,this.handleCurrentChange(this.currentPage,"filter")}),o()(n,"handleCurrentChange",function(e,t){this.currentPage=e;var a={token:this.Cookie.get("token"),page:e,count:this.pageSize};""!==this.freeze&&(a.freeze=this.freeze),""!==this.level&&(a.level=this.level),"filter"==t?this.searchData(a):this.getData()}),o()(n,"formatter",function(e){return e.releasetime=e.releasetime.substr(0,10),e.releasetime}),o()(n,"handleSelectionChange",function(e){this.multipleSelection=e.map(function(e){return e.ID})}),o()(n,"handleEdit",function(e){this.$router.push(""+e)}),o()(n,"handleDelete",function(e){var t=this,a={stfid:e};Object(s.MessageBox)({title:"提示",message:"此操作将永久删除数据, 是否继续？",showCancelButton:!0,confirmButtonText:"确定",cancelButtonText:"取消",beforeClose:function(e,n,l){"confirm"===e?(n.confirmButtonLoading=!0,n.confirmButtonText="执行中...",t.$http({method:"POST",url:"/user/delete_staff/",data:a,params:{token:t.Cookie.get("token")}}).then(function(e){n.confirmButtonLoading=!1,200==e.status?(Object(s.Message)({type:"success",message:e.message,duration:1e3}),t.getData()):Object(s.Message)({type:"error",message:e.message,duration:1e3}),n.confirmButtonLoading=!1,l()})):l()}})}),o()(n,"getData",function(){var e=this;this.loading=!0,this.$http({method:"get",url:"/user/get_user_list/",params:{token:this.Cookie.get("token"),page:this.currentPage,count:this.pageSize}}).then(function(t){200==t.status?t.data?(e.tableData=t.data,e.total=t.all_count):(e.tableData=null,e.total=t.all_count):(e.tableData=null,e.total=t.all_count,Object(s.Message)({type:"error",message:t.message,duration:2e3})),e.loading=!1}).catch(function(){e.loading=!1})}),o()(n,"searchData",function(e){var t=this;this.loading=!0,this.$http({method:"get",url:"/user/get_admin_list/",params:e}).then(function(e){200==e.status?(t.tableData=e.data,t.total=e.all_count):(t.tableData=[],t.total=e.all_count),t.loading=!1}).catch(function(){t.loading=!1})}),o()(n,"searchKeyword",function(){this.currentPage=1,this.handleCurrentChange(this.currentPage)}),n)},c={render:function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"customer-man-container"},[a("div",{staticClass:"announcement-header"},[a("div",{staticClass:"header-left"},[a("b",[e._v("管理")]),e._v(" "),a("span",[e._v("共 "+e._s(e.total)+" 条")])]),e._v(" "),a("div",{staticClass:"header-right"},[e._v("\n            姓名：\n            "),a("el-input",{staticClass:"input-with-select search",attrs:{size:"mini",placeholder:"请输入姓名"},model:{value:e.phone,callback:function(t){e.phone=t},expression:"phone"}},[a("el-button",{attrs:{slot:"append",icon:"el-icon-search",title:"搜索"},on:{click:e.select},slot:"append"})],1),e._v("\n            性别：\n            "),a("el-select",{attrs:{size:"mini",clearable:"",placeholder:"请选择"},on:{change:e.select},model:{value:e.gender,callback:function(t){e.gender=t},expression:"gender"}},[a("el-option",{attrs:{label:"男",value:0}}),e._v(" "),a("el-option",{attrs:{label:"女",value:1}})],1)],1)]),e._v(" "),a("div",{staticClass:"announcement-list"},[a("el-table",{directives:[{name:"loading",rawName:"v-loading",value:e.loading,expression:"loading"}],ref:"multipleTable",staticStyle:{width:"100%"},attrs:{data:e.tableData,"tooltip-effect":"dark",border:"",stripe:""},on:{"selection-change":e.handleSelectionChange}},[a("el-table-column",{attrs:{prop:"usheader",label:"头像",align:"center","show-overflow-tooltip":""},scopedSlots:e._u([{key:"default",fn:function(e){return[a("img",{staticClass:"product-img",attrs:{src:e.row.usheader,alt:""}})]}}])}),e._v(" "),a("el-table-column",{attrs:{prop:"usnickname",label:"昵称",align:"center","show-overflow-tooltip":""}}),e._v(" "),a("el-table-column",{attrs:{prop:"wxprovice",label:"所在省",align:"center","show-overflow-tooltip":""}}),e._v(" "),a("el-table-column",{attrs:{prop:"uscity",label:"所在市",align:"center","show-overflow-tooltip":""}}),e._v(" "),a("el-table-column",{attrs:{prop:"usphone",label:"手机号码",align:"center","show-overflow-tooltip":""}}),e._v(" "),a("el-table-column",{attrs:{prop:"uslastlogin",label:"注册时间",align:"center","show-overflow-tooltip":""},scopedSlots:e._u([{key:"default",fn:function(t){return[a("span",[e._v(e._s(e.filterTime(t.row.uslastlogin)))])]}}])}),e._v(" "),a("el-table-column",{attrs:{prop:"uslastlogin",label:"最近登录时间",align:"center","show-overflow-tooltip":""},scopedSlots:e._u([{key:"default",fn:function(t){return[a("span",[e._v(e._s(e.filterTime(t.row.uslastlogin)))])]}}])})],1),e._v(" "),a("el-pagination",{staticClass:"pagination",attrs:{background:"",layout:"prev, pager, next, jumper, ->","current-page":e.currentPage,"page-size":e.pageSize,total:e.total},on:{"current-change":function(t){e.handleCurrentChange(t,"")},"update:currentPage":function(t){e.currentPage=t}}})],1)])},staticRenderFns:[]};var u=a("VU/8")(r,c,!1,function(e){a("Xdp4")},null,null);t.default=u.exports}});