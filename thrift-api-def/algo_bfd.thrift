namespace cpp bfd
namespace java bfd

service WeiboService {
  double getReview(1: string content),          #return the degree various from 0 to 1 about bad review to good review
  double getSentiment(1: string content),         #return the degree various from 0 to 1 about sentiment
}

