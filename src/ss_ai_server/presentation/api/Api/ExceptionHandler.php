<?php
/**
 * Exception handler for API requests.
 *
 * @package SS_AI_Image_Search
 * @subpackage Api
 */

declare( strict_types=1 );

namespace SS_AI_Image_Search\Api;

use SS_AI_Image_Search\Exceptions\Api\ApiException;
use SS_AI_Image_Search\Exceptions\Api\AuthenticationException;
use SS_AI_Image_Search\Exceptions\Api\NotFoundException;
use SS_AI_Image_Search\Exceptions\Api\ValidationException;
use SS_AI_Image_Search\Exceptions\Api\RateLimitException;
use SS_AI_Image_Search\Exceptions\Api\ServerException;
use SS_AI_Image_Search\Exceptions\Api\TimeoutException;
use SS_AI_Image_Search\Exceptions\Api\ConnectionException;

/**
 * Exception handler class for converting exceptions to responses.
 */
class ExceptionHandler {

	/**
	 * Handle an exception and return a Response.
	 *
	 * @param \Throwable $exception Exception to handle.
	 * @return Response Response object.
	 */
	public function handle( \Throwable $exception ): Response {
		if ( $exception instanceof ApiException ) {
			return Response::from_exception( $exception );
		}

		// Handle specific exception types.
		if ( $exception instanceof AuthenticationException ) {
			return Response::error(
				$exception->getMessage(),
				$exception->get_http_status_code(),
				array( 'code' => $exception->get_code() )
			);
		}

		if ( $exception instanceof ValidationException ) {
			return Response::error(
				$exception->getMessage(),
				$exception->get_http_status_code(),
				$exception->get_errors()
			);
		}

		if ( $exception instanceof NotFoundException ) {
			return Response::error(
				$exception->getMessage(),
				$exception->get_http_status_code()
			);
		}

		if ( $exception instanceof RateLimitException ) {
			return Response::error(
				$exception->getMessage(),
				$exception->get_http_status_code(),
				array( 'retry_after' => $exception->get_retry_after() )
			);
		}

		if ( $exception instanceof TimeoutException ) {
			return Response::error(
				$exception->getMessage(),
				408,
				array( 'timeout' => $exception->get_timeout() )
			);
		}

		if ( $exception instanceof ConnectionException ) {
			return Response::error(
				$exception->getMessage(),
				503,
				array( 'host' => $exception->get_host() )
			);
		}

		if ( $exception instanceof ServerException ) {
			return Response::error(
				$exception->getMessage(),
				$exception->get_http_status_code()
			);
		}

		// Generic exception handling.
		return Response::error(
			'An unexpected error occurred.',
			500,
			array(
				'message' => $exception->getMessage(),
				'file'    => $exception->getFile(),
				'line'    => $exception->getLine(),
			)
		);
	}

	/**
	 * Check if exception should be retried.
	 *
	 * @param \Throwable $exception Exception to check.
	 * @return bool True if should retry.
	 */
	public function should_retry( \Throwable $exception ): bool {
		// Retry on timeout or connection errors.
		if ( $exception instanceof TimeoutException ) {
			return true;
		}

		if ( $exception instanceof ConnectionException ) {
			return true;
		}

		// Retry on 5xx server errors.
		if ( $exception instanceof ServerException ) {
			return $exception->get_http_status_code() >= 500;
		}

		// Retry on rate limit if retry_after is set.
		if ( $exception instanceof RateLimitException ) {
			return $exception->get_retry_after() > 0;
		}

		return false;
	}

	/**
	 * Get retry delay in seconds.
	 *
	 * @param \Throwable $exception Exception to check.
	 * @param int        $attempt_number Current attempt number (1-based).
	 * @return int Delay in seconds.
	 */
	public function get_retry_delay( \Throwable $exception, int $attempt_number ): int {
		// Use exponential backoff.
		$delay = (int) pow( 2, $attempt_number - 1 );

		// If rate limit exception, use the retry_after value.
		if ( $exception instanceof RateLimitException ) {
			$retry_after = $exception->get_retry_after();
			if ( $retry_after > 0 ) {
				return $retry_after;
			}
		}

		// Cap at 60 seconds.
		return min( $delay, 60 );
	}
}