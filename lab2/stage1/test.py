'''
Author: Ashton
Date: 2023-12-13 20:06:07
LastEditors: Ashton
LastEditTime: 2023-12-24 10:54:44
Description: 
'''
import gzip


class triplet_filter:
    def __init__(self, triplet_data, basic_entities, entity_min, entity_max = 20000, releation_min = 50):
        self.triplets = self.process(triplet_data)
        self.triplets = self.filter1()
        self.basic_entities = basic_entities
        self.entity_min = entity_min
        self.entity_max = entity_max
        self.relation_min = releation_min
        (self.entity_count, self.relation_count) = self.count()
        (self.triplets, self.relations) = self.filter2()
        self.extend_entities = self.get_extend_entities()
        self.triplets = self.filler3()

    def process(self, triplet_data):
        triplets = []
        for line in triplet_data:
            line = line.strip()
            triplet = line.split('\t')
            triplets.append(triplet)
        return triplets

    def count(self):
        entity_count = {}
        relation_count = {}
        for triplet in self.triplets:
            if triplet[0] not in entity_count:
                entity_count[triplet[0]] = 1
            else:
                entity_count[triplet[0]] += 1
            if triplet[1] not in relation_count:
                relation_count[triplet[1]] = 1
            else:
                relation_count[triplet[1]] += 1
            if triplet[2] not in entity_count:
                entity_count[triplet[2]] = 1
            else:
                entity_count[triplet[2]] += 1
        return (entity_count, relation_count)

    def filter1(self):
        triplets = []
        for triplet in self.triplets:
            if triplet[0].startswith('<http://rdf.freebase.com/ns/') and triplet[2].startswith('<http://rdf.freebase.com/ns/'):
                triplets.append(triplet)
        return triplets

    def filter2(self):
        triplets = []
        relations = []
        for triplet in self.triplets:
            if self.relation_count[triplet[1]] > self.relation_min:
                triplets.append(triplet)
                relations.append(triplet[1])
        return (triplets, relations)
    
    def get_extend_entities(self):
        extend_entities = set()
        for entity, count in self.entity_count.items():
            if self.entity_min <= count and count <= self.entity_max:
                extend_entities.add(entity)
        return extend_entities
    
    def filler3(self):
        triplets = []
        for triplet in self.triplets:
            if (triplet[0] in self.basic_entities or triplet[0] in self.extend_entities) and (triplet[2] in self.basic_entities or triplet[2] in self.extend_entities):
                triplets.append(triplet)
        return triplets

if __name__ == '__main__':
    movie2fb = {}
    movie_entities = []

    with open('lab2/stage1/data/douban2fb.txt', 'r', encoding = 'utf8') as file:
        for line in file:
            id, fb = line.strip().split()
            movie_entity = '<http://rdf.freebase.com/ns/' + fb + '>'
            movie2fb[id] = movie_entity
            movie_entities.append(movie_entity)
            
    triplets = []
    '''
    with gzip.open('lab2/stage1/data/freebase_douban.gz', 'rb') as file:
        with open('lab2/stage1/data/extract_movie_raw.txt', 'a') as f:
            for line in file:
                line = line.strip()
                triplet = line.decode().split('\t')
                if triplet[0] in movie_entities or triplet[2] in movie_entities:
                    f.write('\t'.join(triplet[0:3]) + '\n')
    '''

    with open('lab2/stage1/data/extract_movie_raw.txt', 'r') as file:
        filter1 = triplet_filter(file.readlines(), movie_entities, 20)
        with open('lab2/stage1/data/extract_movie.txt', 'a') as f:
            for triplet in filter1.triplets:
                f.write('\t'.join(triplet) + '\n')

    extend_entities = filter1.extend_entities
    triplets = []
    '''
    with gzip.open('lab2/stage1/data/freebase_douban.gz', 'rb') as file:
        with open('lab2/stage1/data/extract_extend_raw.txt', 'a') as f:
            for line in file:
                line = line.strip()
                triplet = line.decode().split('\t')
                if triplet[0] in movie_entities or triplet[2] in movie_entities:
                    continue
                if triplet[0] in extend_entities or triplet[2] in extend_entities:
                    f.write('\t'.join(triplet[0:3]) + '\n')'''

    with open('lab2/stage1/data/extract_extend_raw.txt', 'r') as file:
        filter2 = triplet_filter(file.readlines(), extend_entities, 15)
        with open('lab2/stage1/data/extract_extend.txt', 'a') as f:
            for triplet in filter1.triplets:
                f.write('\t'.join(triplet) + '\n')

    with open('lab2/stage1/data/kg.txt', 'a') as file:
        f1 = open('lab2/stage1/data/extract_movie.txt', 'r')
        f2 = open('lab2/stage1/data/extract_extend.txt', 'r')
        for line in f1.readlines():
            file.write(line)
        for line in f2.readlines():
            file.write(line)