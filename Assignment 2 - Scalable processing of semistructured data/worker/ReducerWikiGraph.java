package uniandes.mapRed;

import java.io.IOException;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

//The Reducer receives a list with every person born in a specific place and iterates through them generating
//a String of the format Lugar, [CIUDAD] | Persona, [NOMBRE], [FECHA_DE_NACIMIENTO] which we then use on the 
// web server to generate the graph information in JSON format 
public class WCReducer extends Reducer<Text, Text, Text, Text> {
	@Override
	protected void reduce(Text key, Iterable<Text> values,
			Context context)
			throws IOException, InterruptedException {
		String result ="";
		for(Text s: values){
			result+= s.toString() + " | ";
		}
		context.write(new Text(key + " | "), new Text(result));
		
	}

}
