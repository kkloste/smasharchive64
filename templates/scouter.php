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

     <h1><a href = "\">Smash Archive</a></h1>

     <h2>Full player database</h2>

       &emsp; larger power level = higher estimated skill: boom is 50+, new-comers are ~10</br>
       &emsp; smaller standard deviation = more confidence that power level is accurate:</br>
       &emsp; acc < 1 is high confidence, 2 is reasonably confident, 3+ much less confident</br>


     <h4>=======================================</h4>
     Players listed in descending order of average power level. </br>
     Total number of players in database: {{ rows[1] }} </br>
     Average power level: {{ rows[2] }} </br>

    <br></br>
     <table>
       <tr>
         <th width="48%">Tournament</th>
         <th width="32%">  Date  </th>
         <th width="20%">Entrants</th>
       </tr>
       {% for event in rows[3] %}
         <tr>
              <td align="left"> {{ event[0] }} </td>
              <td align="left"> {{ event[1][0] }}-{{ event[1][1] }}-{{ event[1][2] }} </td>
              <td align="right"> {{ event[2] }} </td>
         </tr>
       {% endfor %}
     </table>

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
