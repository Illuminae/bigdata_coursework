package uniandes.mapRed;

import java.io.IOException;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;
import java.util.concurrent.ThreadLocalRandom;

/* The total wikipedia dataset has approximately 15.82 million pages, so this mapper will emit 
 * pages with a probability of ~ 1m/15.82 = 6.3% to generate the 1m page dataset
 * The random number will be the key, so up to 64 reducers can work in parallel on rebuilding the file
 */
public class WCMapper extends Mapper<LongWritable, Text, IntWritable, Text> {
	
	@Override
	protected void map(LongWritable key, Text value,
			Context context)
			throws IOException, InterruptedException {		
		
		int randomNum = ThreadLocalRandom.current().nextInt(1, 1001);
		if(randomNum < 64){
			context.write(new IntWritable(randomNum), value);
		}

	}
}
