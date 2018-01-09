// Initialize the Amazon Cognito credentials provider.
AWS.config.region = 'us-east-2';
AWS.config.credentials = new AWS.CognitoIdentityCredentials({
    IdentityPoolId: 'us-east-2:e865e713-685c-4f71-986c-3598ce67bcc4',
});

var s3BucketName = 's3.bt2.doublehelix.com';
var s3 = new AWS.S3({
  params: {Bucket: s3BucketName}
});

function uploadFile() {
  var files = document.getElementById('file_upload').files;
  if (!files.length) {
    return alert('Please choose a file to upload first.');
  }

  var folderName = 'demo3';

  var file = files[0];
  var fileName = file.name;
  var folderKey = encodeURIComponent(folderName) + '/';
  var fileKey = folderKey + fileName;
  s3.upload({
      Key: fileKey,
      Body: file,
    }, function(err, data) {
         if (err) {
           return alert('There was an error uploading your file: ', err.message);
         }
         alert('Successfully uploaded file.');
  });
}
