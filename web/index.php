<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="bootstrap.min.css">
  <script src="jquery.min.js"></script>
  <script src="bootstrap.min.js"></script>
    <script src="jquery-1.7.2.min.js" language="javascript"></script>
    <script language="javascript">
        $(document).ready(function () {
            $("#info td:nth-child(4)").each(function () {
                if (parseInt($(this).text(), 10)>45) {
                    $(this).parent("tr").css("background-color", "#e8590c");
                }
            });
        });
    </script>
</head>
<body style="background-color: #000">

<div class="container">
 <u> <h1 align="center" style="color: #ffffff" >PIROBOT</h1> </u>
 <hr>
 <hr>

 <p style="text-align: left; width:49%; display: inline-block;">  <button  type="button" class="btn btn-dark">model_01</button></p>
 <p style="text-align: right; width:50%; display: inline-block;"> <button  type="button" class="btn btn-dark">Light</button></p>

  <hr>
  <div class="table-responsive">          
  <table id="info" class="table table-dark"  >
    <thead>
      <tr>
        <th>Id</th>
        <th>Name</th>
        <th>Phone</th>
        <th>Temp</th>
		<th>Pulse</th>
		<th>photo</th>
      </tr>
    </thead>
    <tbody>
     

<?php
$conn = mysqli_connect("localhost", "root", "", "web");
// Check connection
if ($conn->connect_error) {
die("Connection failed: " . $conn->connect_error);
}
$sql = "SELECT id, name, phone, temp, photo FROM info";
$result = $conn->query($sql);
if ($result->num_rows > 0) {
// output data of each row
while($row = $result->fetch_assoc())
{
echo "<tr>";
echo "<td>" . $row['id'] . "</td>";
echo "<td>" . $row['name'] . "</td>";
echo "<td>" . $row['phone'] . "</td>";
echo "<td>" . $row['temp'] . "</td>";
echo "<td>" . $row['temp'] . "</td>";
echo '<td>' .
      '<img src = "data:image/png;base64,' . base64_encode($row['photo']) . ' "  class="img-circle"  width = "50px" height = "50px"/>'
      . '</td>';
echo "</tr>";
}
} else { echo "0 results"; }
$conn->close();
?>
    </tbody>
  </table>
  </div>
</div>

</body>
</html>