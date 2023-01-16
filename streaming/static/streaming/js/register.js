res = document.getElementById("id_aform_pre-role");
res.remove(1);

document.getElementById("id_aform_pre-role").addEventListener("change", (event) => {
    role_id = event.target.options[event.target.selectedIndex].value;

    if (role_id == 2){
        if(document.getElementById("register_3").style.visibility=="visible"){
            document.getElementById("register_3").style.visibility='hidden';

        }
          document.getElementById("id_cform_pre-subscription").value=1;
         document.getElementById("register_2").style.visibility='visible';
    }else if(role_id==3){
        if(document.getElementById("register_2").style.visibility=="visible"){
            document.getElementById("register_2").style.visibility='hidden';
        }
           document.getElementById("id_bform_pre-name").value = 'hello';
             document.getElementById("id_bform_pre-website").value = 'https://';
             document.getElementById("id_bform_pre-tour_dates").value = 0;
             document.getElementById("id_bform_pre-country").value = 1;
         document.getElementById("register_3").style.visibility='visible';
    }else{
        document.getElementById("register_3").style.visibility='hidden';
        document.getElementById("register_2").style.visibility='hidden';
    }
})