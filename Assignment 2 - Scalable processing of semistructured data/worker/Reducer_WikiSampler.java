package uniandes.mapRed;

import java.io.IOException;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

//The Reducer receives a list with articles, with a random number as key. They are joined to a single 
//string. As for some reason the <page> tag gets lost while reading, we add it again. 
//We output the final string with key "result" so all pages end up in the same tuple
public class WCReducer extends Reducer<IntWritable, Text, Text, Text> {
	@Override
	protected void reduce(IntWritable key, Iterable<Text> values,
			Context context)
			throws IOException, InterruptedException {
		StringBuilder result =new StringBuilder("");
		for(Text s: values){
			result.append("<page>" + s.toString());
		}
		context.write(new Text("result"), new Text(result.toString()));
		
	}

}
