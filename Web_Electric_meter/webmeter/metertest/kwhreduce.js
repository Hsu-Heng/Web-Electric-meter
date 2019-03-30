function kwhreduce(key, values)
{
          var result = 0;
          for (var i = 0; i < values.length; i++) {
              result += values[i].kwh;
              }
          return result;
}
