package uniandes.mapRed;

import java.io.IOException;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

//Reducer sums all the pages found 

public class WCReducer extends Reducer<Text, IntWritable, Text, IntWritable> {
	@Override
	protected void reduce(Text key, Iterable<IntWritable> values,
			Context context)
			throws IOException, InterruptedException {
		int tot=0;
		for(IntWritable iw:values){
			tot+=iw.get();
		}
		context.write(key, new IntWritable(tot));
	}

}
