$(document).ready(function(){

   $(".slidingDiv").hide();
   $(".show_hide").show();

   $('.show_hide').toggle(function(){
       $(".slidingDiv").slideDown(
         function(){
           $("#plus").text("-")
         }
       );
   },function(){
       $(".slidingDiv").slideUp(
       function(){
           $("#plus").text("+")
       }
       );
   });
});