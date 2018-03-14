class EmotionGiver:
	def __init__(self,tp,ep):
		self.tp = tp
		self.ep = ep
		self.ids,self.intervals = self.from_transcription_to_table(self.tp)
		self.id2emotion = self.generate_id_emotion_dict(self.ep)

	def from_transcription_to_table(self,transcription_realpath):
		lines = open(transcription_realpath,'r').readlines()
		ids = [line[0:line.find(' ')] for line in lines]
		intervals = []
		for line in lines:
			s = line.find('[')+1
			e = line.find(']')
			tmp = line[s:e].split('-')
			start = float(tmp[0])
			end = float(tmp[1])
			intervals.append({'start':start,'end':end})
		return (ids,intervals)


	def generate_id_emotion_dict(self,eval_path):
		lines = open(eval_path,'r').readlines()
		id2emotion = {}
		for line in lines:
			tmp = line.split(' ')
			id = tmp[0]
			emotion = tmp[1].strip(':;')
			id2emotion[id] = emotion
		return id2emotion

	def from_curtime_to_utterance_id(self,curtime,ids,time_intervals):
		for i,interval in enumerate(time_intervals):
			if curtime<interval['end'] and curtime>interval['start']:
				return ids[i]
		return -1

	def from_curtime_to_emotion(self,curtime):
		uid = self.from_curtime_to_utterance_id(curtime,self.ids,self.intervals)
		if uid!=-1:
			return self.id2emotion[uid]
		else:
			return 'silent'


if __name__ == '__main__':
	tp = 'E:\\IEMOCAP_full_release\\Session1\\dialog\\transcriptions\\Ses01F_script02_1.txt'
	ep = 'E:\\IEMOCAP_full_release\\Session1\\dialog\\EmoEvaluation\\Categorical\\Ses01F_script02_1_e3_cat.txt'
	eg = EmotionGiver(tp,ep)
	emotion = eg.from_curtime_to_emotion(100)
	print(emotion)