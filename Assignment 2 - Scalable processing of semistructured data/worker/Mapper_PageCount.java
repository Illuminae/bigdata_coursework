package uniandes.mapRed;

import java.io.IOException;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

/*This Mapper will count the number of pages in the wiki dump so that after we can make a proper reduction
 */
public class WCMapper extends Mapper<LongWritable, Text, Text, IntWritable> {
	
	@Override
	protected void map(LongWritable key, Text value,
			Context context)
			throws IOException, InterruptedException {		

		context.write(new Text("Count"), new IntWritable(1));

	}
}
