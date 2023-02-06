#lang racket

;; does not guarantee unique item positions. play thru and test.

(define flag "You've completed the free trial of garbage cleanup simulator! \
Here's a coupon code for 10% off the Premium version: \
maple{saving_the_environment_1092899062}")

(define flag-n (string-length flag))
(define flagdata (map char->integer (string->list flag)))
(define item-chars 64)
(define real-items 30)
(define fake-items 10)
(define xrange '(6 74))
(define yrange '(5 32))
(define rooms 8)

(define (ok-offset _)
  (- (random (+ flag-n item-chars item-chars -1))
     item-chars))

(define (rchar . _) (random 256))

(define offsets
  (let ((cover (range 0 flag-n item-chars)))
    (append
     (sort (append cover
                   (build-list (- real-items (length cover)) ok-offset))
           <)
     (build-list fake-items ok-offset))))


(define rvectors
  (build-list (+ real-items fake-items)
              (λ _ (build-list item-chars rchar))))

(define (oref rvs i c) (list-ref (list-ref rvs i) (- c (list-ref offsets i))))
(define (oset rvs i c v) (list-set rvs i (list-set (list-ref rvs i) (- c (list-ref offsets i)) v)))

(define relevant-items
  (for/list ((c flagdata)
             (i (range flag-n)))
    (shuffle
     (indexes-where (take offsets real-items)
                    (λ (o) (and (<= o i)
                                (> (+ o item-chars) i)))))))

(define fvectors
  (for/fold ((rvip rvectors))
            ((ril relevant-items)
             (c (range flag-n)))
    (oset rvip (first ril) c
          (apply bitwise-xor
                 (cons (list-ref flagdata c)
                       (map (λ (ri) (oref rvip ri c))
                            (rest ril)))))))

;; (define test
;;   (list->string
;;    (for/list ((ril relevant-items)
;;               (c (range flag-n)))
;;      (integer->char
;;       (apply bitwise-xor (map (λ (i) (oref fvectors i c)) ril))))))
;; test

(struct item (rid pos offset data))

(define (pos) (list (apply random xrange) (apply random yrange)))
(define (fakepos)
  (let ((r (pos))
        (f (add1 (random 3))))
    (list
     (if (bitwise-and f 1)
         (+ (first r) (- (second xrange) (first xrange)))
         (first r))
     (if (bitwise-and f 2)
         (+ (second r) (- (second yrange) (first yrange)))
         (second r)))))

(define items
  (for/list ((o offsets)
             (d fvectors)
             (i (range (length offsets))))
    (item (random 0 rooms)
          (if (< i real-items) (pos) (fakepos))
          o
          (string-append "{"
                         (string-join (map (λ (dd) (format "0x~x," dd)) d))
                         "},"))))

(define (item->c i)
  (format "{.rid = ~a, .x = ~a, .y = ~a, .offset = ~a, .data = ~a}"
          (item-rid i)
          (first (item-pos i))
          (second (item-pos i))
          (item-offset i)
          (item-data i)))

(with-output-to-file "item.h" #:exists 'replace
  (λ _ (display (format "\
#include <stdint.h>

#ifndef ITEM_H_
#define ITEM_H_

const int flaglen = ~a;
const int item_total = ~a;
const int item_req = ~a;

typedef struct item_s {
    int rid;
    int x;
    int y;
    int offset;
    uint8_t data[~a];
} item;

item items[] = {
~a
};

#endif // ITEM_H_

" flag-n
  (+ real-items fake-items)
  real-items
  item-chars
  (string-join (map item->c items) ",\n")))))
