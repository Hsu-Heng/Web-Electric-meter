function kwhmap(){
        var key = this.Capaturetime;
        var value = {
          kwh: parseFloat(this.KWH)
        };
         emit(key,value);
       }
