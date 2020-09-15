 $(document).ready(function() {
        // login page 
        $("#username").focus(function() {
            $(".fa-user-cog").addClass("labelfocus");
            $(".fa-user-plus").addClass('labelfocus');
        }).blur(function() {
            $(".fa-user-cog").removeClass("labelfocus");
            $(".fa-user-plus").removeClass("labelfocus")
        });
        // login page
        $("#password").focus(function() {
            $(".fa-user-lock").addClass("labelfocus");
        }).blur(function() {
            $(".fa-user-lock").removeClass("labelfocus");
        });
    });