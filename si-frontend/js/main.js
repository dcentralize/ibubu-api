var token="";

function onSignIn(googleUser) {
 console.log("On Sign In");
  var profile = googleUser.getBasicProfile();

  console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
  console.log('Name: ' + profile.getName());
  console.log('Image URL: ' + profile.getImageUrl());
  console.log('Email: ' + profile.getEmail());


  var profileAuth = googleUser.getAuthResponse();
  token = profileAuth.id_token;
  getUser();
  $('body').load('userData.html');


}
function setup() {
 $.ajax({
        url: "http://localhost:5432/setup",
        type: 'GET',
        success: function(data) {
        $('body').load('#body');
                            }
        });
}
function getUser(){
$('body').load('userData.html');
$.ajax({
    url:"http://localhost:5432/me",
    headers:{'Authorization': 'Token ' + token},
    type:'GET',
    dataType: 'json',
    error: function(data) {
    errorMsg = data;

         if(data.responseJSON.success == false) {
             $('body').load('userData.html');
          }
    },
    success: function(data) {
    userData = data.data;
    $('#userTableBody').append('<tr>'+
                    '<td href="#" onclick="getOrganizations()"><a id="userId" href="#"></a></td>'+

                    '<td id="userFirstname"></td>'+
                    '<td id="userLastname"></td>'+
                    '<td id="userEmail"></td>'+
                    '<td id="userGoogleId"></td>'+
                    '<td>'+
                        '<button onclick="editUserModal()"'+
                                'data-toggle="modal"'+
                                'data-target="#myModal"'+
                                'class="btn btn-default"><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span>'+
                        '</button>'+
                    '</td>'+
                    '<td>'+
                        '<button onclick="deleteUser()"'+
                                'class="btn btn-default"><span class="glyphicon glyphicon-remove"></span>'+
                        '</button>'+
                    '</td>'+
                '</tr>')
            $('#userFirstname').text(userData.firstname);
            $('#userLastname').text(userData.lastname);
            $('#userEmail').text(userData.email);
            $('#userId').text(userData.id);
            $('#userGoogleId').text(userData.google_id)
    }
})
}

function registerUser() {
    var userData;
    $.ajax({
        url:"http://localhost:5432/me",
        headers:{'Authorization': 'Token ' + token},
        type:'POST',
        dataType: 'json',
        success: function(data) {

        $('body').load('userData.html', function(data) {
         getUser();
        });
       }
    })
}
function loadCreateOrganization() {
    $('body').load('createOrganization.html');
}
function getOrganizations() {
      loadCreateOrganization();
      $.ajax({
        url:"http://localhost:5432/me/organizations",
        headers:{'Authorization': 'Token ' + token},
        type:'GET',
        dataType:'json',
        success: function(data) {
           if(data.data.length != 0) {
           $('#tbodyOrganizations').empty();
              for(i=0; i< data.data.length; i++)  {
                    $('#tbodyOrganizations').append('<tr><td>'+data.data[i].id+'</td><td id="organizationName'+data.data[i].id+'">'+data.data[i].name+'</td>'+
                                                        '<td class="editTd"><button data-toggle="modal" data-target="#orgModal" onclick="selectOrganization('+data.data[i].id+')" class="editBtn btn btn-default"><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span></button></td>'+
                                                        '<td class="removeTd"><button onclick="removeOrganization('+data.data[i].id+')" class="removeBtn btn btn-default"><span class="glyphicon glyphicon-remove" aria-hidden="true"></span></button></td>'+
                                                    '</tr>');
                }
            }
        }
      });
}
function createOrganization() {
inputName =$('#inputNameOrganization').val();
    $.ajax({
        url:"http://localhost:5432/me/organizations",
        headers:{'Authorization': 'Token ' + token},
        data:{'name' : inputName},
        type:'POST',
        dataType:'json',
        success: function(data) {
        orgData = data.data;
        getOrganizations();
/*
        $('body').load('organization.html', function(data) {
           $('.orgName').text(orgData.name);
           $('#orgId').text(orgData.id);
        });
        }
        */
        }
    })
    }
function deleteUser() {
     $.ajax({
        url:"http://localhost:5432/me",
        headers:{'Authorization': 'Token ' + token},
        type:'DELETE',
        dataType:'json',
        success: function(data) {
            getUser();
        }
    })
}
function editUserModal(){
    $('#modalInputUserFirstname').attr('value',$('#userFirstname').text());
    $('#modalInputUserEmail').attr('value',$('#userEmail').text());
    $('#modalInputUserLastname').attr('value',$('#userLastname').text());
}

function submitUserChanges() {
    $.ajax({
    url:"http://localhost:5432/me",
    headers:{'Authorization':'Token ' + token},
    data:{'firstname': $('#modalInputUserFirstname').val(),
          'lastname':  $('#modalInputUserLastname').val(),
          'email': $('#modalInputUserEmail').val() },
    type:'PUT',
    dataType:'json',
    success: function(data){
        getUser();

    }

    })
}

function goToHome() {
    getUser();
}
function submitOrganizationChanges() {

    $.ajax({
        url:"http://localhost:5432/organizations/"+selectedOrgId,
        headers:{'Authorization': 'Token ' + token},
        data:{'name': $('#nameEditOrganization').val()},
        type:'PUT',
        dataType:'json',
        success: function(data) {
           getOrganizations();
        }
    })
    selectedOrgId=0;
}

selectedOrgId = 0;

function selectOrganization(id) {
    selectedOrgId=id;
    $('#nameEditOrganization').attr("value",$('#organizationName'+selectedOrgId).text());
}

function removeOrganization(id) {
     $.ajax({
        url:"http://localhost:5432/organizations/"+id,
        headers:{'Authorization': 'Token ' + token},
        type:'DELETE',
        dataType:'json',
        success: function(data) {
           getOrganizations();
        }
     })
}


