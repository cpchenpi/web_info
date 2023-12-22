'''
Author: Ashton
Date: 2023-12-13 20:06:07
LastEditors: Ashton
LastEditTime: 2023-12-22 16:01:19
Description: 
'''
import gzip


class triplet_filter:
    def __init__(self, triplets, basic_entities, entity_min, entity_max = 20000, releation_min = 50):
        self.triplets = triplets
        self.triplets = self.filter1()
        self.basic_entities = basic_entities
        self.entity_min = entity_min
        self.entity_max = entity_max
        self.relation_min = releation_min
        (self.entity_count, self.relation_count) = self.count()
        (self.triplets, self.relations) = self.filter2()
        self.extend_entities = self.get_extend_entities()
        self.triplets = self.filler3()

    def count(self):
        entity_count = {}
        relation_count = {}
        for triplet in self.triplets:
            if triplet[0] not in entity_count:
                entity_count[triplet[0]] = 1
            else:
                entity_count[triplet[0]] += 1
            if triplet[1] not in relation_count:
                relation_count[triplet[2]] = 1
            else:
                relation_count[triplet[2]] += 1
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
            if (triplet[0] in self.basic_entities or triplet[0] in self.extend_entities) and (triplet[2] in self.movie_entities or triplet[2] in self.extend_entities):
                triplets.append(triplet)

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
    with gzip.open('lab2/stage1/data/freebase_douban.gz', 'rb') as file:
        for line in file:
            line = line.strip()
            triplet = line.decode().split('\t')
            if triplet[0] in movie_entities or triplet[2] in movie_entities:
                triplets.append(triplet)
    filter1 = triplet_filter(triplets, movie_entities, 20)

    extend_entities = filter1.extend_entities
    triplets = []
    with gzip.open('lab2/stage1/data/freebase_douban.gz', 'rb') as file:
        for line in file:
            line = line.strip()
            triplet = line.decode().split('\t')
            if triplet[0] in movie_entities or triplet[2] in movie_entities:
                continue
            if triplet[0] in extend_entities or triplet[2] in extend_entities:
                triplets.append(triplet)
    filter2 = triplet_filter(triplets, extend_entities, 15)

    with open('lab2/stage1/data/kg.txt', 'a') as file:
        for triplet in filter1:
            line = triplet[0] + '\t' + triplet[1] + '\t' + triplet[2] + '\n'
            file.write(line)
        for triplet in filter2:
            line = triplet[0] + '\t' + triplet[1] + '\t' + triplet[2] + '\n'
            file.write(line)