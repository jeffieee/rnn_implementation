<?php
// Database connection
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "sampledb"; //change this

$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Query to get the most used programId
$sql = "SELECT programId, COUNT(programId) as usage_count
        FROM residents
        GROUP BY programId
        ORDER BY usage_count DESC
        LIMIT 10";

$result = $conn->query($sql);

$topPrograms = [];
if ($result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        $topPrograms[] = $row;
    }
} else {
    echo "No programs found.";
    exit;
}

// Fetch details for each top programId from programtbl
$programDetails = [];
foreach ($topPrograms as $program) {
    $programId = $program['programId'];
    $sqlProgramDetails = "SELECT * FROM programtbl WHERE programId = '$programId'";
    $resultProgramDetails = $conn->query($sqlProgramDetails);

    if ($resultProgramDetails === FALSE) {
        die("Error: " . $conn->error);
    }

    if ($resultProgramDetails->num_rows > 0) {
        $programDetail = $resultProgramDetails->fetch_assoc();
        $programDetail['usage_count'] = $program['usage_count'];
        $programDetails[] = $programDetail;
    }
}

$conn->close();
?>

<!DOCTYPE html>
<html>
<head>
    <title>Top 10 Programs</title>
</head>
<body>

<h1>Top 10 Program Details</h1>

<table border="1">
    <tr>
        <th>Program ID</th>
        <th>Program Name</th>
        <th>Description</th>
       
    </tr>
    <?php foreach ($programDetails as $detail) { ?>
    <tr>
        <td><?php echo $detail['programId']; ?></td>
        <td><?php echo $detail['programName']; ?></td>
        <td><?php echo $detail['programDescription']; ?></td>

    </tr>
    <?php } ?>
</table>

</body>
</html>