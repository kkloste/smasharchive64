<!doctype html>
<html>

<style>
table, td, th {
    border: 1px solid black;
}
table {
    border-collapse: collapse;
    width: 25%;
}
</style>

   <body>

     <h2><a href = "\">go back to home page</a></h2>

     <h2>Full player database</h2>

       &emsp; larger = higher estimated skill: boom is 50+, new-comers are ~10</br>
       &emsp; smaller = more confidence that power level is accurate:</br>
       &emsp; acc < 1 is high confidence, 2 is reasonably confident, 3+ not enough data to be confident</br>


     <h4>=======================================</h4>
     Players listed in descending order of average power level. </br>
     Total number of players in database: {{ rows[1] }} </br>
     Average power level: {{ rows[2] }} </br>


    <br></br>
    <table>
      <tr>
        <th>Player</th>
        <th>Power level</th>
        <th>Standard deviation</th>
      </tr>
      {% for player in rows[0] %}
        <tr>
            {% for item in player %}
                <td> {{ item }} </td>
            {% endfor %}
        </tr>
      {% endfor %}
    </table>

   </body>
</html>
