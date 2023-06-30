import { TestBed } from '@angular/core/testing';

import { C3DService } from './c3-d.service';

describe('C3DService', () => {
  let service: C3DService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(C3DService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
